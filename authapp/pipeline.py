from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

from django.conf import settings
from django.utils import timezone

import requests
from social_core.exceptions import AuthForbidden

from shutil import copyfile
from authapp.models import User, UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    # api_url = f"https://api.vk.com/method/users.get/fieds=bdate,about,sex&access_token=response{['access_token']}&v='5.92'"
    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))  # то же самое, что строка выше

    resp = requests.get(api_url)

    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
        user.userprofile.gender_no_choice = UserProfile.MALE
    elif data['sex'] == 1:
        user.userprofile.gender = UserProfile.FEMALE
        user.userprofile.gender_no_choice = UserProfile.FEMALE

    if data['about']:
        user.userprofile.about_me = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().year - bdate.year

        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    else:
        age = None

    user.save()

    user_mirror = User.objects.get(id=user.id)
    avatar_path = response.get('photo')

    avatar = requests.get(avatar_path)
    if avatar.status_code != 200:
        return

    avatar_filename = f"{user_mirror.username}_{avatar_path[avatar_path.rfind('/') + 1:avatar_path.rfind('?')]}"
    path_to_save = f'{settings.MEDIA_ROOT}/users_avatars/{avatar_filename}'

    with open(path_to_save, 'wb') as f:
        f.write(avatar.content)
    user_mirror.avatar = path_to_save

    if data['bdate']:
        user_mirror.age = age

    user_mirror.save()

window.onload = function () {
    $('.basket-list').on('click', 'input[type="number"]', function () {
        let elem = event.target;
        $.ajax({
            url: "/baskets/edit/" + elem.name + "/" + elem.value + "/",
            success: function (data) {
                $('.basket-list').html(data.result);
            }
        })
    });
    event.preventDefault();
}
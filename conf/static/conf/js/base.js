$(document).ready(function () {
    $('.navbar-burger, #gray-background').on('click', function (e) {
        $(".navbar-burger, .navbar-menu").toggleClass("is-active");

        $('html').toggleClass('is-clipped');

        $('#gray-background').toggleClass('grey-background');
    });
});
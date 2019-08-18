$(document).ready(function () {
    // Check for click events on the navbar burger icon
    $(".navbar-burger").on('click', function (e) {
        $(".navbar-burger, .navbar-menu").toggleClass("is-active");

        $('html').toggleClass('is-clipped');

        $('#gray-background').toggleClass('grey-background');
    });
});
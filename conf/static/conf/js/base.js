$(document).ready(function () {
    $('.navbar-burger, #gray-background').on('click', function (e) {
        $(".navbar-burger, .navbar-menu").toggleClass("is-active");

        $('html').toggleClass('is-clipped');

        $('#gray-background').toggleClass('grey-background');
    });

    $('#language-selector').on('change', function (e) {
        this.form.submit();
    });

    $('#id_status, #id_club').on('change', function (e) {
        this.form.submit();
    });
});
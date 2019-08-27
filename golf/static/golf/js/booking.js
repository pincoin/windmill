$(document).ready(function () {
    console.log('golf booking');



    $('#id_round_date').datepicker({
        showAnim: '', // turn off animation
        dateFormat: 'yy-mm-dd',
        minDate: +1,
        maxDate: '+1Y',
        beforeShow: function () {
            setTimeout(function () {
                $('.ui-datepicker').css('z-index', 999);
            }, 0);
        }
    });
});
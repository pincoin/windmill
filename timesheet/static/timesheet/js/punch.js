$(document).ready(function () {
    if (!navigator.geolocation) {
        alert('Geolocation is not available.');
    }

    if (navigator.geolocation) {
        console.log('geolocation');
        navigator.geolocation.getCurrentPosition(callback);

        function callback(position) {
            $('input[name=latitude]').val(position.coords.latitude);
            $('input[name=longitude]').val(position.coords.longitude);
        }
    }
});
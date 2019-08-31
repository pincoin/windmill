$(document).ready(function () {
    var club = $('#id_club');
    var agency = $('#id_agency');
    var slot = $('#id_slot');
    var round_date = $('#id_round_date');
    var round_time_hour = $('#id_round_time_hour');

    function get_fee() {
        if (club.val() && round_date.val() && round_time_hour.val()) {
            $.ajax({
                url: '/golf/api/fee/',
                type: 'post',
                dataType: 'json',
                data: {
                    'club_id': parseInt(club.val()),
                    'agency_id': parseInt(agency.val()),
                    'round_date': round_date.val(),
                    'slot': parseInt(slot.val())
                },
                beforeSend: function (xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader('X-CSRFToken', csrftoken);
                    }
                }
            }).done(function (data, textStatus, jqXHR) {
                console.log(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
            });
        }
    }

    round_date.datepicker({
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

    club.on('change', function (e) {
        get_fee();
    });

    round_date.on('change', function (e) {
        get_fee();
    });

    slot.on('change', function (e) {
        round_time_hour.empty();

        switch (parseInt(slot.val())) {
            case 0:
                round_time_hour.append('<option value="6">06</option>'
                    + '<option value="7">07</option>'
                    + '<option value="8">08</option>'
                    + '<option value="9">09</option>'
                    + '<option value="10">10</option>'
                    + '<option value="11">11</option>');
                break;
            case 1:
                round_time_hour.append('<option value="11">11</option>'
                    + '<option value="12">12</option>'
                    + '<option value="13">13</option>'
                    + '<option value="14">14</option>');
                break;
            case 2:
                round_time_hour.append('<option value="15">15</option>');
                break;
            case 3:
                round_time_hour.append('<option value="16">16</option>'
                    + '<option value="17">17</option>'
                    + '<option value="18">18</option>'
                    + '<option value="19">19</option>');
                break;
        }

        get_fee();
    });
});
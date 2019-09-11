function get_fee() {
    let club = $('#id_club');
    let agency = $('#id_agency');
    let slot = $('#id_slot');
    let round_date = $('#id_round_date');
    let round_date_info = $('#id_round_date_info');
    let round_time_hour = $('#id_round_time_hour');
    let fee = $('#id_fee');
    let people = $('#id_people');

    if (club.val() && round_date.val() && round_time_hour.val()) {
        $.ajax({
            url: '/golf/api/fee/',
            type: 'post',
            dataType: 'json',
            data: {
                'club_id': parseInt(club.val()),
                'agency_id': parseInt(agency.val()),
                'round_date': round_date.val().substring(0, 10),
                'slot': parseInt(slot.val())
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        }).done(function (data, textStatus, jqXHR) {
            fee.val(data.fee * people.val());
            round_date_info.val(data.season + '/' + data.day_of_week);
        }).fail(function (data, textStatus, errorThrown) {
            round_date_info.val(data.responseJSON['__all__'][0]['message']);
        });
    }
}

function reset_round_time_hour() {
    let slot = $('#id_slot');
    let round_time_hour = $('#id_round_time_hour');

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
                + '<option value="19">19</option>'
                + '<option value="20">20</option>');
            break;
    }
}

$(document).ready(function () {
    let club = $('#id_club');
    let slot = $('#id_slot');
    let round_date = $('#id_round_date');
    let people = $('#id_people');

    let tee_off_time_form = $('#id_tee_off_time_form');

    round_date.datepicker({
        showAnim: '', // turn off animation
        dateFormat: 'yy-mm-dd (DD)',
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
        reset_round_time_hour();
        get_fee();
    });

    people.on('change', function (e) {
        get_fee();
    });

    $(document).on('click', '#id_tee_off_time_add', function (e) {
        let status_text = $(this).data('status_text');
        let remove_text = $(this).data('remove_text');

        $.ajax({
            url: '/golf/api/tee-off-time/add/',
            type: 'post',
            dataType: 'json',
            data: {
                'booking_uuid': $(this).data('booking_uuid'),
                'offer_tee_off_time_hour': $('#id_offer_tee_off_time_hour').val(),
                'offer_tee_off_time_minute': $('#id_offer_tee_off_time_minute').val(),
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        }).done(function (data, textStatus, jqXHR) {
            if ('tee_off_time_str' in data) {
                tee_off_time_form.prepend("" +
                    "<div class=\"field is-horizontal\">\n" +
                    "   <div class=\"field-label is-normal\"></div>\n" +
                    "   <div class=\"field-body\">\n" +
                    "      <div class=\"field has-addons\">\n" +
                    "         <p class=\"control is-expanded\">\n" +
                    "            <input type=\"text\" value=\"" + data.tee_off_time_str + "\" class=\"input disabled tee_off_time\" disabled=\"\">\n" +
                    "         </p>\n" +
                    "         <p class=\"control\">\n" +
                    "            <a class=\"button is-warning\">\n" +
                    "               <span>" + status_text + "</span>\n" +
                    "            </a>\n" +
                    "         </p>\n" +
                    "         <p class=\"control\">\n" +
                    "            <a class=\"button is-danger tee_off_time_remove\" data-id=\"1\">\n" +
                    "               <span class=\"icon\"><i class=\"far fa-minus-square\"></i></span>\n" +
                    "               <span>" + remove_text + "</span>\n" +
                    "            </a>\n" +
                    "         </p>\n" +
                    "      </div>\n" +
                    "   </div>\n" +
                    "</div>");
            }
        }).fail(function (data, textStatus, errorThrown) {
            console.log(data);
        });
    });

    $(document).on('click', '.tee_off_time_remove', function (e) {
        let tee_off_time_block = $(this).closest('.is-horizontal');

        $.ajax({
            url: '/golf/api/tee-off-time/delete/',
            type: 'post',
            dataType: 'json',
            data: {
                'tee_off_time_pk': $(this).data('id')
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        }).done(function (data, textStatus, jqXHR) {
            tee_off_time_block.remove();
        }).fail(function (data, textStatus, errorThrown) {
            console.log(data);
        });
    });

    $(document).on('click', '.tee_off_time_accept', function (e) {
        let accept_text = $(this).data('accept_text');
        let confirmed_text = $(this).data('confirmed_text');

        let tee_off_time_accept = $('.tee_off_time_accept');

        let confirmed = $(this);

        $.ajax({
            url: '/golf/api/tee-off-time/accept/',
            type: 'post',
            dataType: 'json',
            data: {
                'tee_off_time_pk': $(this).data('id')
            },
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                }
            }
        }).done(function (data, textStatus, jqXHR) {
            if ('tee_off_time_pk' in data) {
                // reset all
                tee_off_time_accept.removeClass('is-primary');
                tee_off_time_accept.addClass('is-warning');
                tee_off_time_accept.children('span:nth-child(2)').text(accept_text);

                // make it confirmed
                confirmed.removeClass('is-warning');
                confirmed.addClass('is-primary');
                confirmed.children('span:nth-child(2)').text(confirmed_text);
            }
        }).fail(function (data, textStatus, errorThrown) {
            console.log(data);
        });
    });
});
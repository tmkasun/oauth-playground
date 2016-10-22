(function ($) {
    $(function () {
        init_role_selection();
        init_pre_submit_messages();
        $('.modal-trigger').leanModal();
    }); // end of document ready
})(jQuery); // end of jQuery name space

function init_pre_submit_messages() {
    $('#try_step_one').leanModal({
        ready: function () {
            $('#selected_auth_endpoint').html($('#auth_endpoint').val());
            modal_closed = false;
            var calls = function () {
                $('#submit_auth').submit();
            };
            var seconds = 25,
                display = $('.pre_info_timer');
            _startTimer(seconds, display, calls);
        },
        complete: function () {
            modal_closed = true;
        }
    });
}
var modal_closed = true;
function _startTimer(duration, display, callback) {
    var timer = duration, minutes, seconds;
    var loop = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.text(minutes + ":" + seconds);
        var timeout = --timer < 0;
        if (timeout && !modal_closed) {
            callback();
            clearInterval(loop);
        } else if (timeout) {
            clearInterval(loop);
        }
    }, 1000);
}

function init_role_selection() {
    var auth_input = $('#auth_endpoint');
    var scope = $('#scope');
    var client_id = $('#client_id');

    function post_init() {
        $('#client_id').replaceWith('<input id="client_id" name="client_id" type="password">');
        client_id = $('#client_id');
        client_id.focusin();
        client_id.val("CAN'T SEE THIS AS A USER");
        scope.focusin();
    }

    $("#wso2_user").change(function () {
        var auth_url = $('#wso2_auth_url').val();
        auth_input.val(auth_url);
        scope.val($('#wso2_scope').val());
        post_init();
    });

    $("#facebook_user").change(function () {
        var auth_url = $('#facebook_auth_url').val();
        auth_input.val(auth_url);
        scope.val($('#facebook_scope').val());
        post_init();
    });
}
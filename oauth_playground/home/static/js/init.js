(function ($) {
    $(function () {
        init_role_selection();
        $('.modal-trigger').leanModal();
    }); // end of document ready
})(jQuery); // end of jQuery name space


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
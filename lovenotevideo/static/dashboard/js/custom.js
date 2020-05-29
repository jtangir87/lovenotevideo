/* CREATE EVENT */
$(function () {
    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: "get",
            dataType: "json",
            beforeSend: function () {
                $("#modal-dashboard .modal-content").html("");
                $("#modal-dashboard").modal("show");
            },
            success: function (data) {
                $("#modal-dashboard .modal-content").html(data.html_form);
            },
        });
    };
    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid) {
                    $("#modal-dashboard").modal("hide");
                } else {
                    $("#modal-dashboard .modal-content").html(data.html_form);
                }
            },
        });
        return false;
    };

    // Contact Workers
    $(".js-create-event").click(loadForm);
    $("#modal-dashboard").on("submit", ".js-create-event-form", saveForm);
});
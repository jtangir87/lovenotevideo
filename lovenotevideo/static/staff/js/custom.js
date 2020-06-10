$(function () {
    var loadDetail = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $('#modal-staff-dash .modal-content').html(data.html_event_detail);
                $('#modal-staff-dash').modal("show");
            }
        })
    }

    $(".js-event-detail").on("click", loadDetail);

})


/* Assign Editor Functions */

$(function () {

    /* Functions */

    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-staff-dash .modal-content").html("");
                $("#modal-staff-dash").modal("show");
            },
            success: function (data) {
                $("#modal-staff-dash .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.form_is_valid) {
                    $("#needEditor tbody").html(data.html_need_editor_list);
                    $("#modal-staff-dash").modal("hide");
                }
                else {
                    $("#modal-staff-dash .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };


    /* Binding */


    // Update Employee Skill
    $("#needEditor").on("click", ".js-assign-editor", loadForm);
    $("#modal-staff-dash").on("submit", ".js-assign-editor-form", saveForm);


});

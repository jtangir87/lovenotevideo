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

/* SET TITLES */
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
                    $("#titlesCard").html(data.html_titles);
                    $("#modal-dashboard").modal("hide");
                } else {
                    $("#modal-dashboard .modal-content").html(data.html_form);
                }
            },
        });
        return false;
    };

    // Contact Workers
    $(".js-set-titles").click(loadForm);
    $("#modal-dashboard").on("submit", ".js-set-titles-form", saveForm);
});


/* CONTACT SUPPORT */
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
                    alert("Support Request Sent. We will contact you within 24 hours!")
                } else {
                    $("#modal-dashboard .modal-content").html(data.html_form);
                }
            },
        });
        return false;
    };

    // Contact Workers
    $(".js-contact-support").click(loadForm);
    $("#modal-dashboard").on("submit", ".js-contact-support-form", saveForm);
});


/* Select Package Functions */
$(function () {
    var loadDetail = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $('#publish-modal .modal-content').html(data.html_package_select);
                $('#publish-modal').modal("show");
            }
        })
    }

    $(".js-package-select").on("click", loadDetail);

})

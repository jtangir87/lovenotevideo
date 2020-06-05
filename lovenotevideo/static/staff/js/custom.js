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

    $("#openProjects").on("click", ".js-event-detail", loadDetail);
    $("#completedProjects").on("click", ".js-event-detail", loadDetail);

})
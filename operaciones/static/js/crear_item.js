$(document).ready(function() {
    $("#modalCreateItem").on('show.bs.modal', function(e) {
        var link = $(e.relatedTarget);
        $(this).find(".modal-content").load(link.attr("href"));
    });

    $("#modalCreateItem").on('submit', 'form', function(e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function() {
                $("#modalCreateItem").modal('hide');
                location.reload(); // or update your table another way
            }
        });
    });
});
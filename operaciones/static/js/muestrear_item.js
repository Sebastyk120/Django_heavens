$(document).ready(function () {

    var itemId = null;

    $('.mover-button').click(function () {
        itemId = $(this).data('item-id');
        $.ajax({
            url: '/operaciones/muestreo_items_create',
            type: 'get',
            data: {'item_id': itemId},
            success: function (data) {
                $('.modal-content').html(data.form);
                $('#moverItemModal').modal('show');
            }
        });
    });

    $(document).on('submit', '#moverItemForm', function (event) {
        event.preventDefault();
        var serializedData = $(this).serialize() + '&item_id=' + itemId;
        console.log(serializedData); // Imprimir los datos serializados
        $.ajax({
            url: '/operaciones/muestreo_items_create',
            type: 'post',
            data: serializedData,
            success: function (data) {
                if (data.success) {
                    $('#moverItemModal').modal('hide');
                    location.reload();
                } else {
                    console.log(data);
                    var errorMessage = data.error;
                    $('#errores').html('<div class="alert alert-danger">' + errorMessage + '</div>');
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.log("AJAX Error: ", textStatus, errorThrown);
            }
        });
    });

});

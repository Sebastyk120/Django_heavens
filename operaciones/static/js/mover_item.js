$(document).ready(function() {
    // Capturar el evento click del botón "Mover"
    $('.btn-mover').on('click', function() {
        // Obtener el ID del item de la fila seleccionada
        var itemId = $(this).data('item-id');
        
        // Asignar el ID del item al campo oculto en el formulario
        $('#form-movimiento' + itemId + ' input[name="item_id"]').val(itemId);
        
        // Abrir el modal
        $('#movimientoModal' + itemId).modal('show');
    });
    
    // Capturar el evento click del botón de envío del formulario dentro del modal
    $('.btn-submit').on('click', function() {
        var formId = $(this).closest('form').attr('id');
        var form = $('#' + formId);
        
        // Realizar una petición AJAX para enviar el formulario
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(response) {
                // Cerrar el modal
                form.closest('.modal').modal('hide');
                
                // Redireccionar a la página de mover_item
                window.location.href = '/operaciones/mover_item/';
            },
            error: function(xhr, textStatus, errorThrown) {
                // Manejar el error de la petición AJAX
                // Mostrar mensajes de error, actualizar la interfaz, etc.
            }
        });
    });
});

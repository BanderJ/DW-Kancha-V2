from bd import conectarse  # Importar la función conectarse

def insertar_detalle_venta(id_usuario, id_producto, cantidad, precio):
    # Conectar a la base de datos
    db = conectarse()
    
    try:
        cursor = db.cursor()
        
        # Llamar al procedimiento almacenado con los parámetros necesarios
        cursor.execute("""
            CALL InsertarDetalleVenta(%s, %s, %s, %s);
        """, (id_usuario, id_producto, cantidad, precio))
        
        # Confirmar los cambios en la base de datos
        db.commit()
    finally:
        cursor.close()  # Cerrar el cursor
        db.close()  # Cerrar la conexión


def obtener_detalles_carrito():
    db = conectarse()
    try:
        cursor = db.cursor()
        # Consulta SQL para obtener los detalles del carrito del usuario
        cursor.execute("""
            SELECT 
                Detalle_venta.idDetVta,
                Producto.descripcion,
                Modelo.nombre AS modelo,
                Talla.nombre AS talla,
                Producto.precio,
                Detalle_venta.cantidad,
                Imagen.imagenPrincipal -- Obtener la imagen principal del producto
            FROM 
                Detalle_venta
            INNER JOIN Producto ON Detalle_venta.idProducto = Producto.idProducto
            INNER JOIN Modelo ON Producto.idModelo = Modelo.idModelo
            INNER JOIN Talla ON Producto.idTalla = Talla.id
            INNER JOIN Imagen ON Producto.idImagen = Imagen.idImagen
            INNER JOIN Carrito ON Detalle_venta.idCarrito = Carrito.idCarrito
            WHERE 
                Carrito.estado = 'P';
        """)
        detalles_carrito = cursor.fetchall()
        return detalles_carrito
    finally:
        cursor.close()
        db.close()


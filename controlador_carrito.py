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
        print("Inserción exitosa")
        
    except Exception as e:
        db.rollback()  # Revertir los cambios en caso de error
        print(f"Error al insertar detalle de venta: {e}")
        
    finally:
        cursor.close()  # Cerrar el cursor
        db.close()  # Cerrar la conexión


def obtener_detalles_carrito(id_usuario):
    conexion = conectarse()
    detalles = []
    try:
        with conexion.cursor() as cursor:
            cursor.execute(""" 
               SELECT 
                    Detalle_venta.idDetVta,
                    Producto.descripcion,
                    Modelo.nombre AS modelo,
                    Talla.nombre AS talla,
                    Producto.precio,
                    Detalle_venta.cantidad,
                    Imagen.imagenPrincipal,
                    (Producto.precio * Detalle_venta.cantidad) AS subtotal_producto,
					Carrito.idCarrito,
                    Producto.idProducto
                FROM 
                    Detalle_venta
                INNER JOIN Producto ON Detalle_venta.idProducto = Producto.idProducto
                INNER JOIN Modelo ON Producto.idModelo = Modelo.idModelo
                INNER JOIN Talla ON Producto.idTalla = Talla.id
                INNER JOIN Imagen ON Producto.idImagen = Imagen.idImagen
                INNER JOIN Carrito ON Detalle_venta.idCarrito = Carrito.idCarrito
                WHERE 
                    Carrito.estado = 'P' AND Carrito.idUsuario = %s;
            """, (id_usuario,))
            
            detalles = cursor.fetchall()
    
    except Exception as e:
        print(f"Error al obtener detalles del carrito: {e}")
    
    finally:
        conexion.close()  # Cerrar la conexión
    return detalles


def eliminar_detalle_venta_bd(id_det_vta, id_producto, id_carrito, id_usuario):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Llamar al procedimiento almacenado
            cursor.execute("""
                CALL EliminarDetalleVenta(%s, %s, %s, %s);
            """, (id_det_vta, id_producto, id_carrito, id_usuario))

            conexion.commit()
            print("Detalle de venta eliminado correctamente y subtotal actualizado.")

    except Exception as e:
        conexion.rollback()
        print(f"Error al eliminar detalle de venta: {e}")
    
    finally:
        conexion.close()
        

def incrementarcantidad(id_det_vta, id_producto, id_carrito, id_usuario):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Actualizar la cantidad del producto en el detalle de venta (incrementar en 1)
            cursor.execute("""
                UPDATE detalle_venta 
                INNER JOIN carrito ON detalle_venta.idCarrito = carrito.idCarrito 
                SET detalle_venta.cantidad = detalle_venta.cantidad + 1 
                WHERE detalle_venta.idDetVta = %s AND detalle_venta.idProducto = %s AND detalle_venta.idCarrito = %s AND carrito.idUsuario = %s;
            """, (id_det_vta, id_producto, id_carrito, id_usuario))
            
            # Llamar al procedimiento almacenado para actualizar el subtotal del carrito
            cursor.execute("CALL actualizar_subtotal_carrito(%s);", (id_carrito,))

            # Confirmar los cambios en la base de datos
            conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar cantidad detalle de venta: {e}")
    finally:
        conexion.close()


def disminuircantidad(id_det_vta, id_producto, id_carrito, id_usuario):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Actualizar la cantidad del producto en el detalle de venta
            cursor.execute("""
                UPDATE detalle_venta 
                INNER JOIN carrito ON detalle_venta.idCarrito = carrito.idCarrito 
                SET detalle_venta.cantidad = detalle_venta.cantidad - 1 
                WHERE detalle_venta.idDetVta = %s AND detalle_venta.idProducto = %s AND detalle_venta.idCarrito = %s AND carrito.idUsuario = %s;
            """, (id_det_vta, id_producto, id_carrito, id_usuario))
            
            # Llamar al procedimiento almacenado para actualizar el subtotal del carrito
            cursor.execute("CALL actualizar_subtotal_carrito(%s);", (id_carrito,))

            # Confirmar los cambios en la base de datos
            conexion.commit()
    except Exception as e:
        conexion.rollback()
        print(f"Error al actualizar cantidad detalle de venta: {e}")
    finally:
        conexion.close()


def obtener_total_carrito(id_usuario):
    conexion = conectarse()
    total_carrito = 0.0
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    SUM(Producto.precio * Detalle_venta.cantidad) AS total_carrito
                FROM
                    Detalle_venta
                INNER JOIN Producto ON Detalle_venta.idProducto = Producto.idProducto
                INNER JOIN Carrito ON Detalle_venta.idCarrito = Carrito.idCarrito
                WHERE 
                    Carrito.estado = 'P' AND Carrito.idUsuario = %s;
            """, (id_usuario,))
            
            resultado = cursor.fetchone()
            if resultado:
                total_carrito = resultado[0] if resultado[0] is not None else 0.0
    
    except Exception as e:
        print(f"Error al obtener el total del carrito: {e}")
    
    finally:
        conexion.close()  # Cerrar la conexión
    return total_carrito

def finalizarCompra_bd(id_carrito,id_Ciudad,direccion, id_usuario):
    conexion = conectarse()
    try:
        with conexion.cursor() as cursor:
            # Llamar al procedimiento almacenado
            cursor.execute("""
                CALL finalizarCompra(%s, %s, %s, %s);
            """, (id_carrito,id_Ciudad,direccion, id_usuario))

            conexion.commit()
            print("Compra realizada")

    except Exception as e:
        conexion.rollback()
        print(f"Error al finalizar venta: {e}")
    
    finally:
        conexion.close()


def obtener_id_carrito(id_usuario):
    conexion = conectarse()
    id_carrito = 0;
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    Carrito.idCarrito
                FROM
                    Detalle_venta
                INNER JOIN Producto ON Detalle_venta.idProducto = Producto.idProducto
                INNER JOIN Carrito ON Detalle_venta.idCarrito = Carrito.idCarrito
                WHERE 
                    Carrito.estado = 'P' AND Carrito.idUsuario = %s;
            """, (id_usuario,))
            
            resultado = cursor.fetchone()
            if resultado:
                id_carrito = resultado[0]
    except Exception as e:
        print(f"Error al obtener el total del carrito: {e}")
    finally:
        conexion.close()  # Cerrar la conexión
    return id_carrito
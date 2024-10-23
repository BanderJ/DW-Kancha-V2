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
        stock_disponible = obtener_stock_producto(id_producto)
        cantidad_actual = obtener_cantidad_actual(id_det_vta)

        # Verificar si al incrementar la cantidad se supera el stock disponible
        if cantidad_actual + 1 > stock_disponible:
            return {"error": "La cantidad no puede exceder el stock disponible."}

        # Incrementar cantidad en la base de datos
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE detalle_venta 
            INNER JOIN carrito ON detalle_venta.idCarrito = carrito.idCarrito 
            SET detalle_venta.cantidad = detalle_venta.cantidad + 1 
            WHERE detalle_venta.idDetVta = %s AND detalle_venta.idProducto = %s AND detalle_venta.idCarrito = %s AND carrito.idUsuario = %s;
        """, (id_det_vta, id_producto, id_carrito, id_usuario))
        
        # Obtener el precio del producto
        cursor.execute("SELECT precio FROM producto WHERE idProducto = %s", (id_producto,))
        precio = cursor.fetchone()[0]
        
        # Calcular el nuevo subtotal
        nuevo_subtotal = (cantidad_actual + 1) * precio

        # Actualizar subtotal del carrito
        cursor.execute("CALL actualizar_subtotal_carrito(%s);", (id_carrito,))
        conexion.commit()

        return {"nueva_cantidad": cantidad_actual + 1, "nuevo_subtotal": nuevo_subtotal}
    except Exception as e:
        conexion.rollback()
        print(f"Error al incrementar cantidad: {e}")
        return {"error": "Error al incrementar cantidad."}
    finally:
        conexion.close()


def disminuircantidad(id_det_vta, id_producto, id_carrito, id_usuario):
    conexion = conectarse()
    try:
        cantidad_actual = obtener_cantidad_actual(id_det_vta)

        # Verificar si al disminuir la cantidad es menor que 1
        if cantidad_actual - 1 < 1:
            return {"error": "La cantidad no puede ser menor a 1."}

        # Disminuir cantidad en la base de datos
        cursor = conexion.cursor()
        cursor.execute("""
            UPDATE detalle_venta 
            INNER JOIN carrito ON detalle_venta.idCarrito = carrito.idCarrito 
            SET detalle_venta.cantidad = detalle_venta.cantidad - 1 
            WHERE detalle_venta.idDetVta = %s AND detalle_venta.idProducto = %s AND detalle_venta.idCarrito = %s AND carrito.idUsuario = %s;
        """, (id_det_vta, id_producto, id_carrito, id_usuario))
        
        # Obtener el precio del producto
        cursor.execute("SELECT precio FROM producto WHERE idProducto = %s", (id_producto,))
        precio = cursor.fetchone()[0]
        
        # Calcular el nuevo subtotal
        nuevo_subtotal = (cantidad_actual - 1) * precio

        # Actualizar subtotal del carrito
        cursor.execute("CALL actualizar_subtotal_carrito(%s);", (id_carrito,))
        conexion.commit()

        return {"nueva_cantidad": cantidad_actual - 1, "nuevo_subtotal": nuevo_subtotal}
    except Exception as e:
        conexion.rollback()
        print(f"Error al disminuir cantidad: {e}")
        return {"error": "Error al disminuir cantidad."}
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



# def obtener_modelos_venta(id_venta,id_usuario):
#     conexion = conectarse()
#     detalles = []
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute(""" 
#                SELECT
#     M.nombre AS modeloNombre -- Nombre del modelo del producto
# FROM Venta V
# JOIN Carrito C ON V.idCarrito = C.idCarrito        -- Relacionamos la venta con el carrito
# JOIN Detalle_venta DV ON C.idCarrito = DV.idCarrito -- Relacionamos el carrito con los detalles de venta
# JOIN Producto P ON DV.idProducto = P.idProducto    -- Relacionamos los detalles de venta con los productos
# JOIN Imagen I ON P.idImagen = I.idImagen           -- Relacionamos el producto con sus imágenes
# JOIN Modelo M ON P.idModelo = M.idModelo           -- Relacionamos el producto con el modelo
# JOIN Usuario U ON C.idUsuario = U.idUsuario        -- Relacionamos el carrito con el usuario
# WHERE V.idVenta = %s                                -- Filtrar por ID de la venta
# AND U.idUsuario = %s;                               -- Filtrar por ID del usuario
#             """, (id_venta,id_usuario,))
            
#             detalles = cursor.fetchall()
    
#     except Exception as e:
#         print(f"Error al obtener detalles del carrito: {e}")
    
#     finally:
#         conexion.close()  # Cerrar la conexión
#     return detalles

# def obtener_id_ventas(id_usuario):
#     conexion = conectarse()
#     detalles = []
#     try:
#         with conexion.cursor() as cursor:
#             cursor.execute(""" 
#                SELECT
#     M.nombre AS modeloNombre -- Nombre del modelo del producto
# FROM Venta V
# JOIN Carrito C ON V.idCarrito = C.idCarrito        -- Relacionamos la venta con el carrito
# JOIN Detalle_venta DV ON C.idCarrito = DV.idCarrito -- Relacionamos el carrito con los detalles de venta
# JOIN Producto P ON DV.idProducto = P.idProducto    -- Relacionamos los detalles de venta con los productos
# JOIN Imagen I ON P.idImagen = I.idImagen           -- Relacionamos el producto con sus imágenes
# JOIN Modelo M ON P.idModelo = M.idModelo           -- Relacionamos el producto con el modelo
# JOIN Usuario U ON C.idUsuario = U.idUsuario        -- Relacionamos el carrito con el usuario
# WHERE V.idVenta = %s                                -- Filtrar por ID de la venta
# AND U.idUsuario = %s;                               -- Filtrar por ID del usuario
#             """, (id_venta,id_usuario,))
            
#             detalles = cursor.fetchall()
    
#     except Exception as e:
#         print(f"Error al obtener detalles del carrito: {e}")
    
#     finally:
#         conexion.close()  # Cerrar la conexión
#     return detalles

# def obtener_ventas_y_detalles(id_usuario):
#     conexion = conectarse()
#     ventas = []
#     try:
#         with conexion.cursor() as cursor:
#             # Obtener todas las ventas del usuario
#             cursor.execute("""
#                 SELECT 
#                     Venta.idVenta, 
#                     Venta.fecha, 
#                     Venta.hora, 
#                     Venta.direccion
#                 FROM 
#                     Venta
#                 INNER JOIN Carrito ON Venta.idCarrito = Carrito.idCarrito
#                 WHERE 
#                     Carrito.idUsuario = %s
#                 ORDER BY Venta.fecha DESC, Venta.hora DESC;
#             """, (id_usuario,))
            
#             ventas_base = cursor.fetchall()

#             for venta in ventas_base:
#                 id_venta = venta[0]
                
#                 # Obtener los detalles de cada venta (productos)
#                 cursor.execute("""
#                     SELECT 
#                         P.descripcion AS nombre,         -- Nombre del producto
#                         M.nombre AS modelo,              -- Nombre del modelo
#                         T.nombre AS talla,               -- Nombre de la talla
#                         P.precio AS precio,              -- Precio del producto
#                         DV.cantidad AS cantidad,         -- Cantidad comprada
#                         I.imagenPrincipal AS imagen      -- Imagen del producto
#                     FROM 
#                         Detalle_venta DV
#                     INNER JOIN Producto P ON DV.idProducto = P.idProducto
#                     INNER JOIN Modelo M ON P.idModelo = M.idModelo
#                     INNER JOIN Talla T ON P.idTalla = T.id
#                     INNER JOIN Imagen I ON P.idImagen = I.idImagen
#                     WHERE 
#                         DV.idCarrito = (
#                             SELECT idCarrito FROM Venta WHERE idVenta = %s
#                         );
#                 """, (id_venta,))
                
#                 productos = cursor.fetchall()

#                 # Convertir cada producto en un diccionario
#                 productos_list = []
#                 for producto in productos:
#                     productos_list.append({
#                         'nombre': producto[0],
#                         'modelo': producto[1],
#                         'talla': producto[2],
#                         'precio': producto[3],
#                         'cantidad': producto[4],
#                         'imagen': producto[5]
#                     })

#                 # Agregar los detalles a la venta
#                 ventas.append({
#                     'idVenta': venta[0],
#                     'fecha': venta[1],
#                     'hora': venta[2],
#                     'direccion': venta[3],
#                     'productos': productos_list
#                 })
    
#     except Exception as e:
#         print(f"Error al obtener ventas y detalles: {e}")
    
#     finally:
#         conexion.close()
    
#     return ventas

def obtener_ventas_y_detalles(id_usuario):
    conexion = conectarse()
    ventas = []
    try:
        with conexion.cursor() as cursor:
            # Obtener todas las ventas del usuario
            cursor.execute("""
                SELECT 
                    Venta.idVenta, 
                    Venta.fecha, 
                    Venta.hora, 
                    Venta.direccion
                FROM 
                    Venta
                INNER JOIN Carrito ON Venta.idCarrito = Carrito.idCarrito
                WHERE 
                    Carrito.idUsuario = %s
                ORDER BY Venta.fecha DESC, Venta.hora DESC;
            """, (id_usuario,))
            
            ventas_base = cursor.fetchall()

            for venta in ventas_base:
                id_venta = venta[0]
                
                # Obtener los detalles de cada venta (productos)
                cursor.execute("""
                    SELECT 
                        P.descripcion AS nombre,        
                        M.nombre AS modelo,             
                        T.nombre AS talla,              
                        P.precio AS precio,             
                        DV.cantidad AS cantidad,        
                        I.imagenPrincipal AS imagen     
                    FROM 
                        Detalle_venta DV
                    INNER JOIN Producto P ON DV.idProducto = P.idProducto
                    INNER JOIN Modelo M ON P.idModelo = M.idModelo
                    INNER JOIN Talla T ON P.idTalla = T.id
                    INNER JOIN Imagen I ON P.idImagen = I.idImagen
                    WHERE 
                        DV.idCarrito = (
                            SELECT idCarrito FROM Venta WHERE idVenta = %s
                        );
                """, (id_venta,))
                
                productos = cursor.fetchall()

                # Convertir cada producto en un diccionario
                productos_list = [
                    {
                        'nombre': producto[0],
                        'modelo': producto[1],
                        'talla': producto[2],
                        'precio': producto[3],
                        'cantidad': producto[4],
                        'imagen': producto[5]
                    }
                    for producto in productos
                ]

                # Agregar los detalles a la venta
                ventas.append({
                    'idVenta': venta[0],
                    'fecha': venta[1],
                    'hora': venta[2],
                    'direccion': venta[3],
                    'productos': productos_list
                })
    
    except Exception as e:
        print(f"Error al obtener ventas y detalles: {e}")
    
    finally:
        conexion.close()
    
    return ventas



# def obtener_imagen_compra_mayor(id_usuario):
#     conexion = conectarse()
#     producto_mayor = None
#     try:
#         with conexion.cursor() as cursor:
#             # Obtener todas las ventas del usuario
#             cursor.execute("""
#                 SELECT 
#                     Venta.idVenta, 
#                     Venta.fecha, 
#                     Venta.hora, 
#                     Venta.direccion
#                 FROM 
#                     Venta
#                 INNER JOIN Carrito ON Venta.idCarrito = Carrito.idCarrito
#                 WHERE 
#                     Carrito.idUsuario = %s
#                 ORDER BY Venta.fecha DESC, Venta.hora DESC;
#             """, (id_usuario,))
            
#             ventas_base = cursor.fetchall()

#             for venta in ventas_base:
#                 id_venta = venta[0]
                
#                 # Obtener el producto con mayor cantidad en esta venta
#                 cursor.execute("""
#                     SELECT 
#                         P.descripcion AS nombre,         -- Nombre del producto
#                         M.nombre AS modelo,              -- Nombre del modelo
#                         T.nombre AS talla,               -- Nombre de la talla
#                         P.precio AS precio,              -- Precio del producto
#                         DV.cantidad AS cantidad,         -- Cantidad comprada
#                         I.imagenPrincipal AS imagen      -- Imagen del producto
#                     FROM 
#                         Detalle_venta DV
#                     INNER JOIN Producto P ON DV.idProducto = P.idProducto
#                     INNER JOIN Modelo M ON P.idModelo = M.idModelo
#                     INNER JOIN Talla T ON P.idTalla = T.id
#                     INNER JOIN Imagen I ON P.idImagen = I.idImagen
#                     WHERE 
#                         DV.idCarrito = (
#                             SELECT idCarrito FROM Venta WHERE idVenta = %s
#                         )
#                     ORDER BY DV.cantidad DESC
#                     LIMIT 1;  -- Solo traemos el producto con mayor cantidad
#                 """, (id_venta,))
                
#                 producto = cursor.fetchone()

#                 # Si este producto tiene más cantidad que el actual producto_mayor
#                 if producto and (producto_mayor is None or producto[4] > producto_mayor['cantidad']):
#                     producto_mayor = {
#                         'nombre': producto[0],
#                         'modelo': producto[1],
#                         'talla': producto[2],
#                         'precio': producto[3],
#                         'cantidad': producto[4],
#                         'imagen': producto[5]
#                     }
    
#     except Exception as e:
#         print(f"Error al obtener el producto con mayor cantidad: {e}")
    
#     finally:
#         conexion.close()
    
#     return producto_mayor


def obtener_stock_producto(id_producto):
    conexion = conectarse()
    stock_disponible = 0
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT stock FROM producto WHERE idProducto = %s", (id_producto,))
            stock_disponible = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al obtener stock del producto: {e}")
    finally:
        conexion.close()
    return stock_disponible

def obtener_cantidad_actual(id_det_vta):
    conexion = conectarse()
    cantidad_actual = 0
    try:
        with conexion.cursor() as cursor:
            cursor.execute("""
                SELECT cantidad FROM detalle_venta 
                WHERE idDetVta = %s;
            """, (id_det_vta,))
            cantidad_actual = cursor.fetchone()[0]
    except Exception as e:
        print(f"Error al obtener la cantidad actual del detalle de venta: {e}")
    finally:
        conexion.close()
    return cantidad_actual


# SELECT cr.idCarrito, usu.idUsuario, usu.nombre, usu.numDoc, vt.direccion, vt.fecha, cr.descuento, cr.subtotal
# from carrito cr inner join usuario usu on cr.idUsuario = usu.idUsuario
# inner join detalle_venta dv on cr.idCarrito = dv.idCarrito
# inner join producto pr on dv.idProducto = pr.idProducto
# inner join venta vt on cr.idCarrito = vt.idCarrito
# where idUsuario = 
-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-10-2024 a las 06:06:39
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `kancha`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `actualizar_subtotal_carrito` (IN `p_idCarrito` INT)   BEGIN
    -- Recalcular el subtotal sumando todos los productos del carrito
    UPDATE Carrito 
    SET subtotal = (
        SELECT COALESCE(SUM(dv.cantidad * dv.precio), 0)
        FROM Detalle_venta dv
        WHERE dv.idCarrito = p_idCarrito
    )
    WHERE idCarrito = p_idCarrito;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `EliminarDetalleVenta` (IN `p_idDetVta` INT, IN `p_idProducto` INT, IN `p_idCarrito` INT, IN `p_idUsuario` INT)   BEGIN
    DECLARE v_estado CHAR(1);
    DECLARE v_subtotal DECIMAL(9,2);

    -- Iniciar la transacción
    START TRANSACTION;

    -- Verificar que el carrito pertenece al usuario y está en estado 'P'
    SELECT estado INTO v_estado
    FROM Carrito
    WHERE idCarrito = p_idCarrito AND idUsuario = p_idUsuario AND estado = 'P';

    IF v_estado = 'P' THEN
        -- Eliminar el detalle de venta basado en la clave compuesta
        DELETE FROM Detalle_venta
        WHERE idDetVta = p_idDetVta AND idProducto = p_idProducto AND idCarrito = p_idCarrito;

        -- Recalcular el subtotal del carrito
        SELECT SUM(cantidad * precio) INTO v_subtotal
        FROM Detalle_venta
        WHERE idCarrito = p_idCarrito;

        -- Si no hay detalles restantes, el subtotal será 0
        IF v_subtotal IS NULL THEN
            SET v_subtotal = 0;
        END IF;

        -- Actualizar el subtotal en el carrito
        UPDATE Carrito
        SET subtotal = v_subtotal
        WHERE idCarrito = p_idCarrito;

        -- Confirmar la transacción
        COMMIT;
    ELSE
        -- Si el carrito no está en estado 'P', deshacer la transacción
        ROLLBACK;
    END IF;
    
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `finalizarCompra` (IN `p_idCarrito` INT, IN `p_idCiudad` INT, IN `p_direccion` VARCHAR(50), IN `p_idUsuario` INT)   BEGIN
    -- Declaración de variables
    DECLARE v_fecha DATE;
    DECLARE v_hora TIME;
    DECLARE v_montoTotal DECIMAL(9,2);
    DECLARE v_idVenta INT;

    -- Variables para iterar sobre los detalles de venta
    DECLARE v_idProducto INT;
    DECLARE v_cantidad INT;
    DECLARE done INT DEFAULT 0;

    -- Cursor para los detalles de venta
    DECLARE cur_detalles CURSOR FOR 
        SELECT idProducto, cantidad FROM Detalle_venta WHERE idCarrito = p_idCarrito;

    -- Handler para cerrar el cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;

    -- Iniciar la transacción
    START TRANSACTION;

    -- Verificar si el carrito pertenece al usuario dado
    IF EXISTS (SELECT 1 FROM Carrito WHERE idCarrito = p_idCarrito AND idUsuario = p_idUsuario) THEN
        
        -- Obtener la fecha y la hora actuales
        SET v_fecha = CURDATE();
        SET v_hora = CURTIME();

        -- Calcular el monto total del carrito
        SELECT (subtotal + igv - descuento) INTO v_montoTotal
        FROM Carrito
        WHERE idCarrito = p_idCarrito;

        -- Cambiar el estado del carrito de 'P' (Proceso) a 'C' (Completado)
        UPDATE Carrito
        SET estado = 'C'
        WHERE idCarrito = p_idCarrito;

        -- Insertar la nueva venta en la tabla Venta
        INSERT INTO Venta (id_distrito, idCarrito, fecha, hora, direccion)
        VALUES (p_idCiudad, p_idCarrito, v_fecha, v_hora, p_direccion);

        -- Obtener el id de la venta recién insertada
        SET v_idVenta = LAST_INSERT_ID();

        -- Iterar sobre los detalles de venta del carrito
        OPEN cur_detalles;

        read_loop: LOOP
            FETCH cur_detalles INTO v_idProducto, v_cantidad;

            -- Si no hay más filas, salir del loop
            IF done = 1 THEN 
                LEAVE read_loop; 
            END IF;

            -- Descontar el stock del producto
            UPDATE Producto
            SET stock = stock - v_cantidad
            WHERE idProducto = v_idProducto;

            -- Verificar que el stock no haya quedado negativo
            IF (SELECT stock FROM Producto WHERE idProducto = v_idProducto) < 0 THEN
                -- Si el stock es negativo, revertir la transacción
                ROLLBACK;
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'Stock insuficiente para el producto.';
                LEAVE read_loop;
            END IF;

        END LOOP;

        CLOSE cur_detalles;

        -- Confirmar la transacción si todo fue exitoso
        COMMIT;

    ELSE
        -- Si el carrito no pertenece al usuario dado, deshacemos la transacción
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El carrito no pertenece al usuario especificado.';
    END IF;

END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `InsertarDetalleVenta` (IN `p_idUsuario` INT, IN `p_idProducto` INT, IN `p_cantidad` INT, IN `p_precio` DECIMAL(9,2))   BEGIN
    DECLARE v_idCarrito INT DEFAULT NULL;
    DECLARE v_igv DECIMAL(9,2);
    DECLARE v_descuento DECIMAL(9,2);
    DECLARE v_subtotal DECIMAL(9,2);
    DECLARE v_existente INT DEFAULT 0;
    
    -- Bloque para evitar inserciones repetidas
    DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        -- Aquí eliminamos el SIGNAL para ver el error original
        SELECT 'Error durante la transacción';
    END;

    START TRANSACTION;

    -- Verificar si existe un carrito con estado 'P' para el usuario
    SELECT idCarrito INTO v_idCarrito
    FROM Carrito
    WHERE idUsuario = p_idUsuario
      AND estado = 'P'
    LIMIT 1;
    
    -- Si no existe un carrito en proceso, se crea uno
    IF v_idCarrito IS NULL THEN
        SET v_igv = 0.18; -- Ajustar si es necesario
        SET v_descuento = 0.00;
        SET v_subtotal = p_cantidad * p_precio;
        
        -- Crear un nuevo carrito
        INSERT INTO Carrito (idUsuario, igv, descuento, subtotal, estado)
        VALUES (p_idUsuario, v_igv, v_descuento, v_subtotal, 'P');
        
        -- Obtener el id del nuevo carrito
        SET v_idCarrito = LAST_INSERT_ID();
    ELSE
        -- Actualizar el subtotal del carrito existente
        UPDATE Carrito
        SET subtotal = subtotal + (p_cantidad * p_precio)
        WHERE idCarrito = v_idCarrito;
    END IF;

    -- Verificar si el producto ya está en el carrito
    SELECT COUNT(*) INTO v_existente
    FROM Detalle_venta
    WHERE idProducto = p_idProducto AND idCarrito = v_idCarrito;

    -- Si el producto ya está en el carrito, actualizar la cantidad
    IF v_existente > 0 THEN
        UPDATE Detalle_venta
        SET cantidad = cantidad + p_cantidad
        WHERE idProducto = p_idProducto AND idCarrito = v_idCarrito;
    ELSE
        -- Insertar el detalle de venta si no existe el producto en el carrito
        INSERT INTO Detalle_venta (idProducto, idCarrito, cantidad, precio)
        VALUES (p_idProducto, v_idCarrito, p_cantidad, p_precio);
    END IF;

    COMMIT;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

CREATE TABLE `carrito` (
  `idCarrito` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `igv` decimal(9,2) NOT NULL,
  `descuento` decimal(9,2) NOT NULL,
  `subtotal` decimal(9,2) NOT NULL,
  `estado` char(1) NOT NULL COMMENT 'P->PROCESO\r\nC->COMPLETADO'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoria`
--

CREATE TABLE `categoria` (
  `idCategoria` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `categoria`
--

INSERT INTO `categoria` (`idCategoria`, `nombre`) VALUES
(1, 'Fútbol'),
(2, 'Básquetbol'),
(3, 'Voleibol'),
(4, 'Running'),
(5, 'Ciclismo'),
(6, 'Tenis'),
(7, 'Golf'),
(8, 'Skateboarding'),
(9, 'Senderismo'),
(10, 'Entrenamiento');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categoriaproducto`
--

CREATE TABLE `categoriaproducto` (
  `CategoriaidCategoria` int(11) NOT NULL,
  `ProductoidProducto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `categoriaproducto`
--

INSERT INTO `categoriaproducto` (`CategoriaidCategoria`, `ProductoidProducto`) VALUES
(1, 3),
(1, 4),
(1, 5),
(1, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `color`
--

CREATE TABLE `color` (
  `idColor` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `color`
--

INSERT INTO `color` (`idColor`, `nombre`) VALUES
(1, 'ROJO'),
(2, 'AZUL'),
(3, 'VERDE'),
(4, 'AMARILLO'),
(5, 'NARANJA'),
(6, 'MORADO'),
(7, 'BLANCO'),
(8, 'GRIS'),
(9, 'NEGRO'),
(10, 'ROSADO'),
(11, 'MARRÓN'),
(12, 'VIOLETA'),
(13, 'CELESTE'),
(14, 'TURQUESA'),
(15, 'DORADO'),
(16, 'PLATEADO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comprobantepago`
--

CREATE TABLE `comprobantepago` (
  `idComprobante` int(11) NOT NULL,
  `idVenta` int(11) NOT NULL,
  `montoTotal` int(11) NOT NULL,
  `idTipoComprobante` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamento`
--

CREATE TABLE `departamento` (
  `id_departamento` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `departamento`
--

INSERT INTO `departamento` (`id_departamento`, `nombre`) VALUES
(1, 'Amazonas'),
(2, 'Áncash'),
(3, 'Apurímac'),
(4, 'Arequipa'),
(5, 'Ayacucho'),
(6, 'Cajamarca'),
(7, 'Callao'),
(8, 'Cusco'),
(9, 'Huancavelica'),
(10, 'Huánuco'),
(11, 'Ica'),
(12, 'Junín'),
(13, 'La Libertad'),
(14, 'Lambayeque'),
(15, 'Lima'),
(16, 'Loreto'),
(17, 'Madre de Dios'),
(18, 'Moquegua'),
(19, 'Pasco'),
(20, 'Piura'),
(21, 'Puno'),
(22, 'San Martín'),
(23, 'Tacna'),
(24, 'Tumbes'),
(25, 'Ucayali');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `idDetVta` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL,
  `idCarrito` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio` decimal(9,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `distrito`
--

CREATE TABLE `distrito` (
  `id_distrito` int(11) NOT NULL,
  `id_provincia` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `distrito`
--

INSERT INTO `distrito` (`id_distrito`, `id_provincia`, `nombre`) VALUES
(1, 1, 'Chachapoyas'),
(2, 1, 'Asunción'),
(3, 1, 'Balsas'),
(4, 1, 'Cheto'),
(5, 1, 'Chiliquín'),
(6, 1, 'Chuquibamba'),
(7, 1, 'Granada'),
(8, 1, 'Huancas'),
(9, 1, 'La Jalca'),
(10, 1, 'Leimebamba'),
(11, 1, 'Levanto'),
(12, 1, 'Magdalena'),
(13, 1, 'Mariscal Castilla'),
(14, 1, 'Molinopampa'),
(15, 1, 'Montevideo'),
(16, 1, 'Olleros'),
(17, 1, 'Quinjalca'),
(18, 1, 'San Francisco de Daguas'),
(19, 1, 'San Isidro de Maino'),
(20, 1, 'Soloco'),
(21, 1, 'Sonche'),
(22, 2, 'Bagua'),
(23, 2, 'Aramango'),
(24, 2, 'Copallín'),
(25, 2, 'El Parco'),
(26, 2, 'Imaza'),
(27, 2, 'La Peca'),
(28, 3, 'Jumbilla'),
(29, 3, 'Chisquilla'),
(30, 3, 'Churuja'),
(31, 3, 'Corosha'),
(32, 3, 'Cuispes'),
(33, 3, 'Florida'),
(34, 3, 'Jazán'),
(35, 3, 'Recta'),
(36, 3, 'San Carlos'),
(37, 3, 'Shipasbamba'),
(38, 3, 'Valera'),
(39, 3, 'Yambrasbamba'),
(40, 4, 'Nieva'),
(41, 4, 'El Cenepa'),
(42, 4, 'Río Santiago'),
(43, 5, 'Lamud'),
(44, 5, 'Camporredondo'),
(45, 5, 'Cocabamba'),
(46, 5, 'Colcamar'),
(47, 5, 'Conila'),
(48, 5, 'Inguilpata'),
(49, 5, 'Longuita'),
(50, 5, 'Lonya Chico'),
(51, 5, 'Luya'),
(52, 5, 'Luya Viejo'),
(53, 5, 'María'),
(54, 5, 'Ocalli'),
(55, 5, 'Ocumal'),
(56, 5, 'Pisuquía'),
(57, 5, 'Providencia'),
(58, 5, 'San Cristóbal'),
(59, 5, 'San Francisco del Yeso'),
(60, 5, 'San Jerónimo'),
(61, 5, 'San Juan de Lopecancha'),
(62, 5, 'Santa Catalina'),
(63, 5, 'Santo Tomás'),
(64, 5, 'Tingo'),
(65, 5, 'Trita'),
(66, 6, 'San Nicolás'),
(67, 6, 'Chirimoto'),
(68, 6, 'Cochamal'),
(69, 6, 'Huambo'),
(70, 6, 'Limabamba'),
(71, 6, 'Longar'),
(72, 6, 'Mariscal Benavides'),
(73, 6, 'Milan'),
(74, 6, 'Omia'),
(75, 6, 'Santa Rosa'),
(76, 6, 'Totora'),
(77, 7, 'Bagua Grande'),
(78, 7, 'Cajaruro'),
(79, 7, 'Cumba'),
(80, 7, 'El Milagro'),
(81, 7, 'Jamalca'),
(82, 7, 'Lonya Grande'),
(83, 7, 'Yamón'),
(84, 8, 'Huaraz'),
(85, 8, 'Cochabamba'),
(86, 8, 'Colcabamba'),
(87, 8, 'Huanchay'),
(88, 8, 'Independencia'),
(89, 8, 'Jangas'),
(90, 8, 'La Libertad'),
(91, 8, 'Olleros'),
(92, 8, 'Pampas Grande'),
(93, 8, 'Pariacoto'),
(94, 8, 'Pira'),
(95, 8, 'Tarica'),
(96, 9, 'Aija'),
(97, 9, 'Coris'),
(98, 9, 'Huacllán'),
(99, 9, 'La Merced'),
(100, 9, 'Succha'),
(101, 10, 'Llamellín'),
(102, 10, 'Aczo'),
(103, 10, 'Chaccho'),
(104, 10, 'Chingas'),
(105, 10, 'Mirgas'),
(106, 10, 'San Juan de Rontoy'),
(107, 11, 'Chacas'),
(108, 11, 'Acochaca'),
(109, 12, 'Chiquián'),
(110, 12, 'Abelardo Pardo Lezameta'),
(111, 12, 'Antonio Raymondi'),
(112, 12, 'Aquia'),
(113, 12, 'Cajacay'),
(114, 12, 'Canis'),
(115, 12, 'Colquioc'),
(116, 12, 'Huallanca'),
(117, 12, 'Huasta'),
(118, 12, 'Huayllacayán'),
(119, 12, 'La Primavera'),
(120, 12, 'Mangas'),
(121, 12, 'Pacllón'),
(122, 12, 'San Miguel de Corpanqui'),
(123, 12, 'Ticllos'),
(124, 13, 'Carhuaz'),
(125, 13, 'Acopampa'),
(126, 13, 'Amashca'),
(127, 13, 'Anta'),
(128, 13, 'Ataquero'),
(129, 13, 'Marcara'),
(130, 13, 'Pariahuanca'),
(131, 13, 'San Miguel de Aco'),
(132, 13, 'Shilla'),
(133, 13, 'Tinco'),
(134, 13, 'Yungar'),
(135, 14, 'San Luis'),
(136, 14, 'San Nicolás'),
(137, 14, 'Yauya'),
(138, 15, 'Casma'),
(139, 15, 'Buenavista Alta'),
(140, 15, 'Comandante Noel'),
(141, 15, 'Yaután'),
(142, 16, 'Corongo'),
(143, 16, 'Aco'),
(144, 16, 'Bambas'),
(145, 16, 'Cusca'),
(146, 16, 'La Pampa'),
(147, 16, 'Yanac'),
(148, 16, 'Yupan'),
(149, 17, 'Huari'),
(150, 17, 'Anra'),
(151, 17, 'Cajay'),
(152, 17, 'Chavín de Huantar'),
(153, 17, 'Huacachi'),
(154, 17, 'Huacchis'),
(155, 17, 'Huachis'),
(156, 17, 'Huantar'),
(157, 17, 'Masin'),
(158, 17, 'Paucas'),
(159, 17, 'Ponto'),
(160, 17, 'Rahuapampa'),
(161, 17, 'Rapayán'),
(162, 17, 'San Marcos'),
(163, 17, 'San Pedro de Chaná'),
(164, 17, 'Uco'),
(165, 18, 'Huarmey'),
(166, 18, 'Cochapeti'),
(167, 18, 'Culebras'),
(168, 18, 'Huayan'),
(169, 18, 'Malvas'),
(170, 19, 'Caraz'),
(171, 19, 'Huallanca'),
(172, 19, 'Huata'),
(173, 19, 'Huaylas'),
(174, 19, 'Mato'),
(175, 19, 'Pamparomas'),
(176, 19, 'Pueblo Libre'),
(177, 19, 'Santa Cruz'),
(178, 19, 'Santo Toribio'),
(179, 19, 'Yuracmarca'),
(180, 20, 'Piscobamba'),
(181, 20, 'Casca'),
(182, 20, 'Eleazar Guzmán Barrón'),
(183, 20, 'Fidel Olivas Escudero'),
(184, 20, 'Llama'),
(185, 20, 'Llumpa'),
(186, 20, 'Lucma'),
(187, 20, 'Musga'),
(188, 21, 'Ocros'),
(189, 21, 'Acas'),
(190, 21, 'Cajamarquilla'),
(191, 21, 'Carhuapampa'),
(192, 21, 'Cochas'),
(193, 21, 'Congas'),
(194, 21, 'Llipa'),
(195, 21, 'San Cristóbal de Rajan'),
(196, 21, 'San Pedro'),
(197, 21, 'Santiago de Chilcas'),
(198, 22, 'Cabana'),
(199, 22, 'Bolognesi'),
(200, 22, 'Conchucos'),
(201, 22, 'Huacaschuque'),
(202, 22, 'Huandoval'),
(203, 22, 'Lacabamba'),
(204, 22, 'Llapo'),
(205, 22, 'Pallasca'),
(206, 22, 'Pampas'),
(207, 22, 'Santa Rosa'),
(208, 22, 'Tauca'),
(209, 23, 'Pomabamba'),
(210, 23, 'Huayllán'),
(211, 23, 'Parobamba'),
(212, 23, 'Quinuabamba'),
(213, 24, 'Recuay'),
(214, 24, 'Catac'),
(215, 24, 'Cotaparaco'),
(216, 24, 'Huayllapampa'),
(217, 24, 'Llacllín'),
(218, 24, 'Marca'),
(219, 24, 'Pampas Chico'),
(220, 24, 'Pararín'),
(221, 24, 'Tapacocha'),
(222, 24, 'Ticapampa'),
(223, 25, 'Chimbote'),
(224, 25, 'Cáceres del Perú'),
(225, 25, 'Coishco'),
(226, 25, 'Macate'),
(227, 25, 'Moro'),
(228, 25, 'Nepeña'),
(229, 25, 'Samanco'),
(230, 25, 'Santa'),
(231, 26, 'Sihuas'),
(232, 26, 'Acobamba'),
(233, 26, 'Alfonso Ugarte'),
(234, 26, 'Cashapampa'),
(235, 26, 'Chingalpo'),
(236, 26, 'Huayllabamba'),
(237, 26, 'Quiches'),
(238, 26, 'Ragash'),
(239, 26, 'San Juan'),
(240, 26, 'Sicsibamba'),
(241, 27, 'Yungay'),
(242, 27, 'Cascapara'),
(243, 27, 'Mancos'),
(244, 27, 'Matacoto'),
(245, 27, 'Quillo'),
(246, 27, 'Ranrahirca'),
(247, 27, 'Shupluy'),
(248, 27, 'Yanama'),
(249, 28, 'Abancay'),
(250, 28, 'Chacoche'),
(251, 28, 'Circa'),
(252, 28, 'Curahuasi'),
(253, 28, 'Huanipaca'),
(254, 28, 'Lambrama'),
(255, 28, 'Pichirhua'),
(256, 28, 'San Pedro de Cachora'),
(257, 28, 'Tamburco'),
(258, 29, 'Andahuaylas'),
(259, 29, 'Andarapa'),
(260, 29, 'Chiara'),
(261, 29, 'Huancarama'),
(262, 29, 'Huancaray'),
(263, 29, 'Huayana'),
(264, 29, 'Kishuara'),
(265, 29, 'Pacobamba'),
(266, 29, 'Pacucha'),
(267, 29, 'Pampachiri'),
(268, 29, 'Pomacocha'),
(269, 29, 'San Antonio de Cachi'),
(270, 29, 'San Jerónimo'),
(271, 29, 'San Miguel de Chaccrapampa'),
(272, 29, 'Santa María de Chicmo'),
(273, 29, 'Talavera'),
(274, 29, 'Tumay Huaraca'),
(275, 29, 'Turpo'),
(276, 29, 'Kaquiabamba'),
(277, 29, 'José María Arguedas'),
(278, 30, 'Antabamba'),
(279, 30, 'El Oro'),
(280, 30, 'Huaquirca'),
(281, 30, 'Juan Espinoza Medrano'),
(282, 30, 'Oropesa'),
(283, 30, 'Pachaconas'),
(284, 30, 'Sabaino'),
(285, 31, 'Chalhuanca'),
(286, 31, 'Capaya'),
(287, 31, 'Caraybamba'),
(288, 31, 'Chapimarca'),
(289, 31, 'Colcabamba'),
(290, 31, 'Cotaruse'),
(291, 31, 'Ihuayllo'),
(292, 31, 'Justo Apu Sahuaraura'),
(293, 31, 'Lucre'),
(294, 31, 'Pocohuanca'),
(295, 31, 'San Juan de Chacña'),
(296, 31, 'Sañayca'),
(297, 31, 'Soraya'),
(298, 31, 'Tapairihua'),
(299, 31, 'Tintay'),
(300, 31, 'Toraya'),
(301, 31, 'Yanaca'),
(302, 32, 'Tambobamba'),
(303, 32, 'Cotabambas'),
(304, 32, 'Coyllurqui'),
(305, 32, 'Haquira'),
(306, 32, 'Mara'),
(307, 32, 'Challhuahuacho'),
(308, 33, 'Chincheros'),
(309, 33, 'Anco_Huallo'),
(310, 33, 'Cocharcas'),
(311, 33, 'Huaccana'),
(312, 33, 'Ocobamba'),
(313, 33, 'Ongoy'),
(314, 33, 'Ranracancha'),
(315, 33, 'Uranmarca'),
(316, 34, 'Chuquibambilla'),
(317, 34, 'Curpahuasi'),
(318, 34, 'Gamarra'),
(319, 34, 'Huayllati'),
(320, 34, 'Mamara'),
(321, 34, 'Micaela Bastidas'),
(322, 34, 'Pataypampa'),
(323, 34, 'Progreso'),
(324, 34, 'San Antonio'),
(325, 34, 'Turpay'),
(326, 34, 'Vilcabamba'),
(327, 34, 'Virundo'),
(328, 34, 'Curasco'),
(329, 35, 'Arequipa'),
(330, 35, 'Alto Selva Alegre'),
(331, 35, 'Cayma'),
(332, 35, 'Cerro Colorado'),
(333, 35, 'Characato'),
(334, 35, 'Chiguata'),
(335, 35, 'Jacobo Hunter'),
(336, 35, 'La Joya'),
(337, 35, 'Mariano Melgar'),
(338, 35, 'Miraflores'),
(339, 35, 'Mollebaya'),
(340, 35, 'Paucarpata'),
(341, 35, 'Pocsi'),
(342, 35, 'Polobaya'),
(343, 35, 'Quequeña'),
(344, 35, 'Sabandía'),
(345, 35, 'Sachaca'),
(346, 35, 'San Juan de Siguas'),
(347, 35, 'San Juan de Tarucani'),
(348, 35, 'Santa Isabel de Siguas'),
(349, 35, 'Santa Rita de Siguas'),
(350, 35, 'Socabaya'),
(351, 35, 'Tiabaya'),
(352, 35, 'Uchumayo'),
(353, 35, 'Vitor'),
(354, 35, 'Yanahuara'),
(355, 35, 'Yarabamba'),
(356, 35, 'Yura'),
(357, 36, 'Camaná'),
(358, 36, 'José María Quimper'),
(359, 36, 'Mariano Nicolás Valcárcel'),
(360, 36, 'Mariscal Cáceres'),
(361, 36, 'Nicolás de Piérola'),
(362, 36, 'Ocoña'),
(363, 36, 'Quilca'),
(364, 36, 'Samuel Pastor'),
(365, 37, 'Caravelí'),
(366, 37, 'Acarí'),
(367, 37, 'Atico'),
(368, 37, 'Atiquipa'),
(369, 37, 'Bella Unión'),
(370, 37, 'Cahuacho'),
(371, 37, 'Chala'),
(372, 37, 'Chaparra'),
(373, 37, 'Huanuhuanu'),
(374, 37, 'Jaqui'),
(375, 37, 'Lomas'),
(376, 37, 'Quicacha'),
(377, 37, 'Yauca'),
(378, 38, 'Aplao'),
(379, 38, 'Andagua'),
(380, 38, 'Ayo'),
(381, 38, 'Chachas'),
(382, 38, 'Chilcaymarca'),
(383, 38, 'Choco'),
(384, 38, 'Huancarqui'),
(385, 38, 'Machaguay'),
(386, 38, 'Orcopampa'),
(387, 38, 'Pampacolca'),
(388, 38, 'Tipan'),
(389, 38, 'Uñon'),
(390, 38, 'Uraca'),
(391, 38, 'Viraco'),
(392, 39, 'Chivay'),
(393, 39, 'Achoma'),
(394, 39, 'Cabanaconde'),
(395, 39, 'Callalli'),
(396, 39, 'Caylloma'),
(397, 39, 'Coporaque'),
(398, 39, 'Huambo'),
(399, 39, 'Huanca'),
(400, 39, 'Ichupampa'),
(401, 39, 'Lari'),
(402, 39, 'Lluta'),
(403, 39, 'Maca'),
(404, 39, 'Madrigal'),
(405, 39, 'San Antonio de Chuca'),
(406, 39, 'Sibayo'),
(407, 39, 'Tapay'),
(408, 39, 'Tisco'),
(409, 39, 'Tuti'),
(410, 39, 'Yanque'),
(411, 40, 'Chuquibamba'),
(412, 40, 'Andaray'),
(413, 40, 'Cayarani'),
(414, 40, 'Chichas'),
(415, 40, 'Iray'),
(416, 40, 'Río Grande'),
(417, 40, 'Salamanca'),
(418, 40, 'Yanaquihua'),
(419, 41, 'Mollendo'),
(420, 41, 'Cocachacra'),
(421, 41, 'Dean Valdivia'),
(422, 41, 'Islay'),
(423, 41, 'Mejía'),
(424, 41, 'Punta de Bombón'),
(425, 42, 'Cotahuasi'),
(426, 42, 'Alca'),
(427, 42, 'Charcana'),
(428, 42, 'Huaynacotas'),
(429, 42, 'Pampamarca'),
(430, 42, 'Puyca'),
(431, 42, 'Quechualla'),
(432, 42, 'Sayla'),
(433, 42, 'Tauría'),
(434, 42, 'Tomepampa'),
(435, 42, 'Toro'),
(436, 43, 'Ayacucho'),
(437, 43, 'Acocro'),
(438, 43, 'Acos Vinchos'),
(439, 43, 'Carmen Alto'),
(440, 43, 'Chiara'),
(441, 43, 'Jesús Nazareno'),
(442, 43, 'Ocros'),
(443, 43, 'Pacaycasa'),
(444, 43, 'Quinua'),
(445, 43, 'San José de Ticllas'),
(446, 43, 'San Juan Bautista'),
(447, 43, 'Santiago de Pischa'),
(448, 43, 'Socos'),
(449, 43, 'Tambillo'),
(450, 43, 'Vinchos'),
(451, 43, 'Andrés Avelino Cáceres Dorregaray'),
(452, 44, 'Cangallo'),
(453, 44, 'Chuschi'),
(454, 44, 'Los Morochucos'),
(455, 44, 'María Parado de Bellido'),
(456, 44, 'Paras'),
(457, 44, 'Totos'),
(458, 45, 'Sancos'),
(459, 45, 'Carapo'),
(460, 45, 'Sacsamarca'),
(461, 45, 'Santiago de Lucanamarca'),
(462, 46, 'Huanta'),
(463, 46, 'Ayahuanco'),
(464, 46, 'Huamanguilla'),
(465, 46, 'Iguain'),
(466, 46, 'Luricocha'),
(467, 46, 'Santillana'),
(468, 46, 'Sivia'),
(469, 46, 'Llochegua'),
(470, 46, 'Canayre'),
(471, 46, 'Uchuraccay'),
(472, 46, 'Pucacolpa'),
(473, 46, 'Chaca'),
(474, 47, 'San Miguel'),
(475, 47, 'Anco'),
(476, 47, 'Ayna'),
(477, 47, 'Chilcas'),
(478, 47, 'Chungui'),
(479, 47, 'Luis Carranza'),
(480, 47, 'Santa Rosa'),
(481, 47, 'Tambo'),
(482, 47, 'Samugari'),
(483, 47, 'Anchihuay'),
(484, 47, 'Oronccoy'),
(485, 48, 'Puquio'),
(486, 48, 'Aucará'),
(487, 48, 'Cabana'),
(488, 48, 'Carmen Salcedo'),
(489, 48, 'Chaviña'),
(490, 48, 'Chipao'),
(491, 48, 'Huac-Huas'),
(492, 48, 'Laramate'),
(493, 48, 'Leoncio Prado'),
(494, 48, 'Llauta'),
(495, 48, 'Lucanas'),
(496, 48, 'Ocaña'),
(497, 48, 'Otoca'),
(498, 48, 'Saisa'),
(499, 48, 'San Cristóbal'),
(500, 48, 'San Juan'),
(501, 48, 'San Pedro'),
(502, 48, 'San Pedro de Palco'),
(503, 48, 'Sancos'),
(504, 48, 'Santa Ana de Huaycahuacho'),
(505, 48, 'Santa Lucía'),
(506, 49, 'Coracora'),
(507, 49, 'Chumpi'),
(508, 49, 'Coronel Castañeda'),
(509, 49, 'Pacapausa'),
(510, 49, 'Pullo'),
(511, 49, 'Puyusca'),
(512, 49, 'San Francisco de Ravacayco'),
(513, 49, 'Upahuacho'),
(514, 50, 'Pausa'),
(515, 50, 'Colta'),
(516, 50, 'Corculla'),
(517, 50, 'Lampa'),
(518, 50, 'Marcabamba'),
(519, 50, 'Oyolo'),
(520, 50, 'Pararca'),
(521, 50, 'San Javier de Alpabamba'),
(522, 50, 'San José de Ushua'),
(523, 50, 'Sara Sara'),
(524, 51, 'Querobamba'),
(525, 51, 'Belén'),
(526, 51, 'Chalcos'),
(527, 51, 'Chilcayoc'),
(528, 51, 'Huacaña'),
(529, 51, 'Morcolla'),
(530, 51, 'Paico'),
(531, 51, 'San Pedro de Larcay'),
(532, 51, 'San Salvador de Quije'),
(533, 51, 'Santiago de Paucaray'),
(534, 51, 'Soras'),
(535, 52, 'Huancapi'),
(536, 52, 'Alcamenca'),
(537, 52, 'Apongo'),
(538, 52, 'Asquipata'),
(539, 52, 'Canaria'),
(540, 52, 'Cayara'),
(541, 52, 'Colca'),
(542, 52, 'Huamanquiquia'),
(543, 52, 'Huancaraylla'),
(544, 52, 'Huaya'),
(545, 52, 'Sarhua'),
(546, 52, 'Vilcanchos'),
(547, 53, 'Vilcas Huamán'),
(548, 53, 'Accomarca'),
(549, 53, 'Carhuanca'),
(550, 53, 'Concepción'),
(551, 53, 'Huambalpa'),
(552, 53, 'Independencia'),
(553, 53, 'Saurama'),
(554, 53, 'Vischongo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `favoritos`
--

CREATE TABLE `favoritos` (
  `idCliente` int(11) NOT NULL,
  `idProducto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero`
--

CREATE TABLE `genero` (
  `idGenero` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `genero`
--

INSERT INTO `genero` (`idGenero`, `nombre`) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Niño'),
(4, 'Niña'),
(5, 'Unisex');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `imagen`
--

CREATE TABLE `imagen` (
  `idImagen` int(11) NOT NULL,
  `imagenPrincipal` text NOT NULL,
  `imagenSec01` text NOT NULL,
  `imagenSec02` text NOT NULL,
  `imagenSec03` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `imagen`
--

INSERT INTO `imagen` (`idImagen`, `imagenPrincipal`, `imagenSec01`, `imagenSec02`, `imagenSec03`) VALUES
(1, 'foto (71).webp', 'foto (71).webp', 'foto (72).webp', 'foto (73).webp'),
(2, 'foto (103).avif', 'foto (103).avif', 'foto (104).avif', 'foto (105).avif'),
(3, 'foto (71).webp', 'foto (71).webp', 'foto (72).webp', 'foto (73).webp'),
(4, 'foto (65).webp', 'foto (65).webp', 'foto (66).webp', 'foto (67).webp'),
(5, 'foto (68).webp', 'foto (68).webp', 'foto (69).webp', 'foto (70).webp'),
(6, 'foto (103).avif', 'foto (103).avif', 'foto (104).avif', 'foto (105).avif');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `marca`
--

CREATE TABLE `marca` (
  `idMarca` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `imagen` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `marca`
--

INSERT INTO `marca` (`idMarca`, `nombre`, `imagen`) VALUES
(1, 'Adidas', 'adidas_logo.svg'),
(2, 'Nike', 'nike_logo.svg'),
(3, 'Puma', 'puma_logo.svg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `modelo`
--

CREATE TABLE `modelo` (
  `idModelo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `idMarca` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `modelo`
--

INSERT INTO `modelo` (`idModelo`, `nombre`, `idMarca`) VALUES
(1, 'UltraBoost 21', 1),
(2, 'Superstar', 2),
(3, 'Air Max 90', 2),
(4, 'Air Jordan 1', 2),
(5, 'Suede Classic', 3),
(6, 'Future Rider', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nivelusuario`
--

CREATE TABLE `nivelusuario` (
  `idNivelUsuario` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `puntosRequeridos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci COMMENT='0-999 ->Hierro   \r\n1000-2499->Bronce  5%\r\n2500-4999->Plata 7.5%\r\n5000-  ∞ --> Oro 10%';

--
-- Volcado de datos para la tabla `nivelusuario`
--

INSERT INTO `nivelusuario` (`idNivelUsuario`, `nombre`, `puntosRequeridos`) VALUES
(1, 'Basico', 100);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `idProducto` int(11) NOT NULL,
  `precio` decimal(9,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `descripcion` text NOT NULL,
  `idModelo` int(11) NOT NULL,
  `idTalla` int(11) NOT NULL,
  `idImagen` int(11) NOT NULL,
  `idTipo` int(11) NOT NULL,
  `idGenero` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`idProducto`, `precio`, `stock`, `descripcion`, `idModelo`, `idTalla`, `idImagen`, `idTipo`, `idGenero`) VALUES
(3, 199.99, 6, 'Zapatillas Nike SuperStar para jugar futbol', 2, 5, 3, 1, 1),
(4, 199.99, 4, 'Zapatillas Nike SuperStar para jugar futbol', 2, 6, 4, 1, 1),
(5, 199.99, 27, 'Zapatillas Nike SuperStar para jugar futbol', 2, 7, 5, 1, 1),
(6, 299.99, 6, 'Zapatillas chimpuneras, ideales para jugar futbol en canchas sinteticas', 1, 5, 6, 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_color`
--

CREATE TABLE `producto_color` (
  `idProducto` int(11) NOT NULL,
  `idColor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `producto_color`
--

INSERT INTO `producto_color` (`idProducto`, `idColor`) VALUES
(3, 15),
(4, 8),
(5, 10),
(6, 2),
(6, 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `provincia`
--

CREATE TABLE `provincia` (
  `id_provincia` int(11) NOT NULL,
  `id_departamento` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `provincia`
--

INSERT INTO `provincia` (`id_provincia`, `id_departamento`, `nombre`) VALUES
(1, 1, 'Chachapoyas'),
(2, 1, 'Bagua'),
(3, 1, 'Bongará'),
(4, 1, 'Condorcanqui'),
(5, 1, 'Luya'),
(6, 1, 'Rodríguez de Mendoza'),
(7, 1, 'Utcubamba'),
(8, 2, 'Huaraz'),
(9, 2, 'Aija'),
(10, 2, 'Antonio Raymondi'),
(11, 2, 'Asunción'),
(12, 2, 'Bolognesi'),
(13, 2, 'Carhuaz'),
(14, 2, 'Carlos Fermín Fitzcarrald'),
(15, 2, 'Casma'),
(16, 2, 'Corongo'),
(17, 2, 'Huari'),
(18, 2, 'Huarmey'),
(19, 2, 'Huaylas'),
(20, 2, 'Mariscal Luzuriaga'),
(21, 2, 'Ocros'),
(22, 2, 'Pallasca'),
(23, 2, 'Pomabamba'),
(24, 2, 'Recuay'),
(25, 2, 'Santa'),
(26, 2, 'Sihuas'),
(27, 2, 'Yungay'),
(28, 3, 'Abancay'),
(29, 3, 'Andahuaylas'),
(30, 3, 'Antabamba'),
(31, 3, 'Aymaraes'),
(32, 3, 'Cotabambas'),
(33, 3, 'Chincheros'),
(34, 3, 'Grau'),
(35, 4, 'Arequipa'),
(36, 4, 'Camaná'),
(37, 4, 'Caravelí'),
(38, 4, 'Castilla'),
(39, 4, 'Caylloma'),
(40, 4, 'Condesuyos'),
(41, 4, 'Islay'),
(42, 4, 'La Unión'),
(43, 5, 'Huamanga'),
(44, 5, 'Cangallo'),
(45, 5, 'Huanca Sancos'),
(46, 5, 'Huanta'),
(47, 5, 'La Mar'),
(48, 5, 'Lucanas'),
(49, 5, 'Parinacochas'),
(50, 5, 'Páucar del Sara Sara'),
(51, 5, 'Sucre'),
(52, 5, 'Víctor Fajardo'),
(53, 5, 'Vilcas Huamán'),
(54, 6, 'Cajamarca'),
(55, 6, 'Cajabamba'),
(56, 6, 'Celendín'),
(57, 6, 'Chota'),
(58, 6, 'Contumazá'),
(59, 6, 'Cutervo'),
(60, 6, 'Hualgayoc'),
(61, 6, 'Jaén'),
(62, 6, 'San Ignacio'),
(63, 6, 'San Marcos'),
(64, 6, 'San Miguel'),
(65, 6, 'San Pablo'),
(66, 6, 'Santa Cruz'),
(67, 7, 'Callao'),
(68, 8, 'Cusco'),
(69, 8, 'Acomayo'),
(70, 8, 'Anta'),
(71, 8, 'Calca'),
(72, 8, 'Canas'),
(73, 8, 'Canchis'),
(74, 8, 'Chumbivilcas'),
(75, 8, 'Espinar'),
(76, 8, 'La Convención'),
(77, 8, 'Paruro'),
(78, 8, 'Paucartambo'),
(79, 8, 'Quispicanchi'),
(80, 8, 'Urubamba'),
(81, 9, 'Huancavelica'),
(82, 9, 'Acobamba'),
(83, 9, 'Angaraes'),
(84, 9, 'Castrovirreyna'),
(85, 9, 'Churcampa'),
(86, 9, 'Huaytará'),
(87, 9, 'Tayacaja'),
(88, 10, 'Huánuco'),
(89, 10, 'Ambo'),
(90, 10, 'Dos de Mayo'),
(91, 10, 'Huacaybamba'),
(92, 10, 'Huamalíes'),
(93, 10, 'Leoncio Prado'),
(94, 10, 'Marañón'),
(95, 10, 'Pachitea'),
(96, 10, 'Puerto Inca'),
(97, 10, 'Lauricocha'),
(98, 10, 'Yarowilca'),
(99, 11, 'Ica'),
(100, 11, 'Chincha'),
(101, 11, 'Nasca'),
(102, 11, 'Palpa'),
(103, 11, 'Pisco'),
(104, 12, 'Huancayo'),
(105, 12, 'Concepción'),
(106, 12, 'Chanchamayo'),
(107, 12, 'Jauja'),
(108, 12, 'Junín'),
(109, 12, 'Satipo'),
(110, 12, 'Tarma'),
(111, 12, 'Yauli'),
(112, 12, 'Chupaca'),
(113, 13, 'Trujillo'),
(114, 13, 'Ascope'),
(115, 13, 'Bolívar'),
(116, 13, 'Chepén'),
(117, 13, 'Gran Chimú'),
(118, 13, 'Julcán'),
(119, 13, 'Otuzco'),
(120, 13, 'Pacasmayo'),
(121, 13, 'Pataz'),
(122, 13, 'Sánchez Carrión'),
(123, 13, 'Santiago de Chuco'),
(124, 13, 'Virú'),
(125, 14, 'Chiclayo'),
(126, 14, 'Ferreñafe'),
(127, 14, 'Lambayeque'),
(128, 15, 'Lima'),
(129, 15, 'Barranca'),
(130, 15, 'Cajatambo'),
(131, 15, 'Canta'),
(132, 15, 'Cañete'),
(133, 15, 'Huaral'),
(134, 15, 'Huarochirí'),
(135, 15, 'Huaura'),
(136, 15, 'Oyón'),
(137, 15, 'Yauyos'),
(138, 16, 'Maynas'),
(139, 16, 'Alto Amazonas'),
(140, 16, 'Datem del Marañón'),
(141, 16, 'Loreto'),
(142, 16, 'Mariscal Ramón Castilla'),
(143, 16, 'Putumayo'),
(144, 16, 'Requena'),
(145, 16, 'Ucayali'),
(146, 17, 'Tambopata'),
(147, 17, 'Manu'),
(148, 17, 'Tahuamanu'),
(149, 18, 'Mariscal Nieto'),
(150, 18, 'General Sánchez Cerro'),
(151, 18, 'Ilo'),
(152, 19, 'Pasco'),
(153, 19, 'Daniel Alcides Carrión'),
(154, 19, 'Oxapampa'),
(155, 20, 'Piura'),
(156, 20, 'Ayabaca'),
(157, 20, 'Huancabamba'),
(158, 20, 'Morropón'),
(159, 20, 'Paita'),
(160, 20, 'Sechura'),
(161, 20, 'Sullana'),
(162, 20, 'Talara'),
(163, 21, 'Puno'),
(164, 21, 'Azángaro'),
(165, 21, 'Carabaya'),
(166, 21, 'Chucuito'),
(167, 21, 'El Collao'),
(168, 21, 'Huancané'),
(169, 21, 'Lampa'),
(170, 21, 'Melgar'),
(171, 21, 'Moho'),
(172, 21, 'San Antonio de Putina'),
(173, 21, 'San Román'),
(174, 21, 'Sandia'),
(175, 21, 'Yunguyo'),
(176, 22, 'Moyobamba'),
(177, 22, 'Bellavista'),
(178, 22, 'El Dorado'),
(179, 22, 'Huallaga'),
(180, 22, 'Lamas'),
(181, 22, 'Mariscal Cáceres'),
(182, 22, 'Picota'),
(183, 22, 'Rioja'),
(184, 22, 'San Martín'),
(185, 22, 'Tocache'),
(186, 23, 'Tacna'),
(187, 23, 'Candarave'),
(188, 23, 'Jorge Basadre'),
(189, 23, 'Tarata'),
(190, 24, 'Tumbes'),
(191, 24, 'Contralmirante Villar'),
(192, 24, 'Zarumilla'),
(193, 25, 'Coronel Portillo'),
(194, 25, 'Atalaya'),
(195, 25, 'Padre Abad'),
(196, 25, 'Purús');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reseña`
--

CREATE TABLE `reseña` (
  `idReseña` int(11) NOT NULL,
  `ClienteidCliente` int(11) NOT NULL,
  `ProductoidProducto` int(11) NOT NULL,
  `escala` int(1) NOT NULL,
  `fecha` date NOT NULL,
  `descripcion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `talla`
--

CREATE TABLE `talla` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `talla`
--

INSERT INTO `talla` (`id`, `nombre`) VALUES
(1, '36'),
(2, '37'),
(3, '38'),
(4, '39'),
(5, '40'),
(6, '41'),
(7, '42'),
(8, '43'),
(9, '44'),
(10, '45'),
(11, '46');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipocomprobante`
--

CREATE TABLE `tipocomprobante` (
  `idTipoComprobante` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipousuario`
--

CREATE TABLE `tipousuario` (
  `idTipoUsuario` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `tipousuario`
--

INSERT INTO `tipousuario` (`idTipoUsuario`, `nombre`) VALUES
(1, 'Administrador'),
(2, 'Cliente'),
(3, 'Invitado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_producto`
--

CREATE TABLE `tipo_producto` (
  `idTipo` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `tipo_producto`
--

INSERT INTO `tipo_producto` (`idTipo`, `nombre`) VALUES
(1, 'Chimpunes'),
(2, 'Zapatillas'),
(3, 'Chimpuneras'),
(4, 'Urbanas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `idTipoUsuario` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `numDoc` varchar(20) DEFAULT NULL,
  `apePat` varchar(50) DEFAULT NULL,
  `apeMat` varchar(50) DEFAULT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(50) DEFAULT NULL,
  `telefono` char(9) DEFAULT NULL,
  `fechaNacimiento` date DEFAULT NULL,
  `sexo` char(1) DEFAULT NULL COMMENT 'F->femenino\r\nM->masculino\r\nN->no especificado',
  `idNivelUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `idTipoUsuario`, `nombre`, `numDoc`, `apePat`, `apeMat`, `correo`, `password`, `telefono`, `fechaNacimiento`, `sexo`, `idNivelUsuario`) VALUES
(1, 1, 'Juan', '12345678', 'Pérez', 'Gómez', 'juan.perez@gmail.com', 'password123', '987654321', '1990-01-01', 'M', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `venta`
--

CREATE TABLE `venta` (
  `idVenta` int(11) NOT NULL,
  `idCarrito` int(11) NOT NULL,
  `id_distrito` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `direccion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD PRIMARY KEY (`idCarrito`),
  ADD KEY `FKCarrito875014` (`idUsuario`);

--
-- Indices de la tabla `categoria`
--
ALTER TABLE `categoria`
  ADD PRIMARY KEY (`idCategoria`);

--
-- Indices de la tabla `categoriaproducto`
--
ALTER TABLE `categoriaproducto`
  ADD PRIMARY KEY (`CategoriaidCategoria`,`ProductoidProducto`),
  ADD KEY `FKCategoriaP106442` (`ProductoidProducto`);

--
-- Indices de la tabla `color`
--
ALTER TABLE `color`
  ADD PRIMARY KEY (`idColor`);

--
-- Indices de la tabla `comprobantepago`
--
ALTER TABLE `comprobantepago`
  ADD PRIMARY KEY (`idComprobante`),
  ADD KEY `FKComprobant934284` (`idVenta`),
  ADD KEY `FKComprobant835227` (`idTipoComprobante`);

--
-- Indices de la tabla `departamento`
--
ALTER TABLE `departamento`
  ADD PRIMARY KEY (`id_departamento`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`idDetVta`,`idProducto`,`idCarrito`),
  ADD KEY `FKDetalle_ve685353` (`idCarrito`),
  ADD KEY `FKDetalle_ve347889` (`idProducto`);

--
-- Indices de la tabla `distrito`
--
ALTER TABLE `distrito`
  ADD PRIMARY KEY (`id_distrito`),
  ADD KEY `FKDistrito467621` (`id_provincia`);

--
-- Indices de la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD PRIMARY KEY (`idCliente`,`idProducto`),
  ADD KEY `FKFavoritos426683` (`idProducto`);

--
-- Indices de la tabla `genero`
--
ALTER TABLE `genero`
  ADD PRIMARY KEY (`idGenero`);

--
-- Indices de la tabla `imagen`
--
ALTER TABLE `imagen`
  ADD PRIMARY KEY (`idImagen`);

--
-- Indices de la tabla `marca`
--
ALTER TABLE `marca`
  ADD PRIMARY KEY (`idMarca`);

--
-- Indices de la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD PRIMARY KEY (`idModelo`),
  ADD KEY `FKModelo452020` (`idMarca`);

--
-- Indices de la tabla `nivelusuario`
--
ALTER TABLE `nivelusuario`
  ADD PRIMARY KEY (`idNivelUsuario`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`idProducto`),
  ADD KEY `FKProducto553495` (`idTalla`),
  ADD KEY `FKProducto919561` (`idModelo`),
  ADD KEY `FKProducto273856` (`idImagen`),
  ADD KEY `FKProducto130523` (`idTipo`),
  ADD KEY `FKProducto56164` (`idGenero`);

--
-- Indices de la tabla `producto_color`
--
ALTER TABLE `producto_color`
  ADD PRIMARY KEY (`idProducto`,`idColor`),
  ADD KEY `FKProducto_C794711` (`idColor`);

--
-- Indices de la tabla `provincia`
--
ALTER TABLE `provincia`
  ADD PRIMARY KEY (`id_provincia`),
  ADD KEY `FKProvincia956653` (`id_departamento`);

--
-- Indices de la tabla `reseña`
--
ALTER TABLE `reseña`
  ADD PRIMARY KEY (`idReseña`,`ClienteidCliente`,`ProductoidProducto`),
  ADD KEY `FKReseña738255` (`ClienteidCliente`),
  ADD KEY `FKReseña400882` (`ProductoidProducto`);

--
-- Indices de la tabla `talla`
--
ALTER TABLE `talla`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipocomprobante`
--
ALTER TABLE `tipocomprobante`
  ADD PRIMARY KEY (`idTipoComprobante`);

--
-- Indices de la tabla `tipousuario`
--
ALTER TABLE `tipousuario`
  ADD PRIMARY KEY (`idTipoUsuario`);

--
-- Indices de la tabla `tipo_producto`
--
ALTER TABLE `tipo_producto`
  ADD PRIMARY KEY (`idTipo`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`),
  ADD KEY `FKUsuario557876` (`idTipoUsuario`),
  ADD KEY `FKUsuario54363` (`idNivelUsuario`);

--
-- Indices de la tabla `venta`
--
ALTER TABLE `venta`
  ADD PRIMARY KEY (`idVenta`),
  ADD KEY `FKVenta19082` (`idCarrito`),
  ADD KEY `FKVenta449236` (`id_distrito`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carrito`
--
ALTER TABLE `carrito`
  MODIFY `idCarrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `categoria`
--
ALTER TABLE `categoria`
  MODIFY `idCategoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `color`
--
ALTER TABLE `color`
  MODIFY `idColor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `comprobantepago`
--
ALTER TABLE `comprobantepago`
  MODIFY `idComprobante` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `departamento`
--
ALTER TABLE `departamento`
  MODIFY `id_departamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `distrito`
--
ALTER TABLE `distrito`
  MODIFY `id_distrito` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=555;

--
-- AUTO_INCREMENT de la tabla `genero`
--
ALTER TABLE `genero`
  MODIFY `idGenero` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `imagen`
--
ALTER TABLE `imagen`
  MODIFY `idImagen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `marca`
--
ALTER TABLE `marca`
  MODIFY `idMarca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `modelo`
--
ALTER TABLE `modelo`
  MODIFY `idModelo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `nivelusuario`
--
ALTER TABLE `nivelusuario`
  MODIFY `idNivelUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `idProducto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `provincia`
--
ALTER TABLE `provincia`
  MODIFY `id_provincia` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=197;

--
-- AUTO_INCREMENT de la tabla `talla`
--
ALTER TABLE `talla`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tipocomprobante`
--
ALTER TABLE `tipocomprobante`
  MODIFY `idTipoComprobante` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipousuario`
--
ALTER TABLE `tipousuario`
  MODIFY `idTipoUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipo_producto`
--
ALTER TABLE `tipo_producto`
  MODIFY `idTipo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `venta`
--
ALTER TABLE `venta`
  MODIFY `idVenta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `carrito`
--
ALTER TABLE `carrito`
  ADD CONSTRAINT `FKCarrito875014` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `categoriaproducto`
--
ALTER TABLE `categoriaproducto`
  ADD CONSTRAINT `FKCategoriaP106442` FOREIGN KEY (`ProductoidProducto`) REFERENCES `producto` (`idProducto`),
  ADD CONSTRAINT `FKCategoriaP322739` FOREIGN KEY (`CategoriaidCategoria`) REFERENCES `categoria` (`idCategoria`);

--
-- Filtros para la tabla `comprobantepago`
--
ALTER TABLE `comprobantepago`
  ADD CONSTRAINT `FKComprobant835227` FOREIGN KEY (`idTipoComprobante`) REFERENCES `tipocomprobante` (`idTipoComprobante`),
  ADD CONSTRAINT `FKComprobant934284` FOREIGN KEY (`idVenta`) REFERENCES `venta` (`idVenta`);

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `FKDetalle_ve347889` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`),
  ADD CONSTRAINT `FKDetalle_ve685353` FOREIGN KEY (`idCarrito`) REFERENCES `carrito` (`idCarrito`);

--
-- Filtros para la tabla `distrito`
--
ALTER TABLE `distrito`
  ADD CONSTRAINT `FKDistrito467621` FOREIGN KEY (`id_provincia`) REFERENCES `provincia` (`id_provincia`);

--
-- Filtros para la tabla `favoritos`
--
ALTER TABLE `favoritos`
  ADD CONSTRAINT `FKFavoritos21291` FOREIGN KEY (`idCliente`) REFERENCES `usuario` (`idUsuario`),
  ADD CONSTRAINT `FKFavoritos426683` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`);

--
-- Filtros para la tabla `modelo`
--
ALTER TABLE `modelo`
  ADD CONSTRAINT `FKModelo452020` FOREIGN KEY (`idMarca`) REFERENCES `marca` (`idMarca`);

--
-- Filtros para la tabla `producto`
--
ALTER TABLE `producto`
  ADD CONSTRAINT `FKProducto130523` FOREIGN KEY (`idTipo`) REFERENCES `tipo_producto` (`idTipo`),
  ADD CONSTRAINT `FKProducto273856` FOREIGN KEY (`idImagen`) REFERENCES `imagen` (`idImagen`),
  ADD CONSTRAINT `FKProducto553495` FOREIGN KEY (`idTalla`) REFERENCES `talla` (`id`),
  ADD CONSTRAINT `FKProducto56164` FOREIGN KEY (`idGenero`) REFERENCES `genero` (`idGenero`),
  ADD CONSTRAINT `FKProducto919561` FOREIGN KEY (`idModelo`) REFERENCES `modelo` (`idModelo`);

--
-- Filtros para la tabla `producto_color`
--
ALTER TABLE `producto_color`
  ADD CONSTRAINT `FKProducto_C794711` FOREIGN KEY (`idColor`) REFERENCES `color` (`idColor`),
  ADD CONSTRAINT `FKProducto_C895005` FOREIGN KEY (`idProducto`) REFERENCES `producto` (`idProducto`);

--
-- Filtros para la tabla `provincia`
--
ALTER TABLE `provincia`
  ADD CONSTRAINT `FKProvincia956653` FOREIGN KEY (`id_departamento`) REFERENCES `departamento` (`id_departamento`);

--
-- Filtros para la tabla `reseña`
--
ALTER TABLE `reseña`
  ADD CONSTRAINT `FKReseña400882` FOREIGN KEY (`ProductoidProducto`) REFERENCES `producto` (`idProducto`),
  ADD CONSTRAINT `FKReseña738255` FOREIGN KEY (`ClienteidCliente`) REFERENCES `usuario` (`idUsuario`);

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `FKUsuario54363` FOREIGN KEY (`idNivelUsuario`) REFERENCES `nivelusuario` (`idNivelUsuario`),
  ADD CONSTRAINT `FKUsuario557876` FOREIGN KEY (`idTipoUsuario`) REFERENCES `tipousuario` (`idTipoUsuario`);

--
-- Filtros para la tabla `venta`
--
ALTER TABLE `venta`
  ADD CONSTRAINT `FKVenta19082` FOREIGN KEY (`idCarrito`) REFERENCES `carrito` (`idCarrito`),
  ADD CONSTRAINT `FKVenta449236` FOREIGN KEY (`id_distrito`) REFERENCES `distrito` (`id_distrito`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

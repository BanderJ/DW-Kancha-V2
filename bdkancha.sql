CREATE TABLE Reseña (
    idReseña int(11) NOT NULL, 
    ClienteidCliente int(11) NOT NULL, 
    ProductoidProducto int(11) NOT NULL, 
    escala int(1) NOT NULL, 
    fecha date NOT NULL, 
    descripcion varchar(255) NOT NULL, 
    PRIMARY KEY (idReseña, ClienteidCliente, ProductoidProducto)
);

CREATE TABLE Usuario (
    idUsuario int(11) NOT NULL AUTO_INCREMENT, 
    idTipoUsuario int(11) NOT NULL, 
    nombre varchar(50) NOT NULL, 
    numDoc varchar(20), 
    apePat varchar(50), 
    apeMat varchar(50), 
    correo varchar(50) NOT NULL, 
    password varchar(50), 
    idNivelUsuario int(11) NOT NULL, 
    PRIMARY KEY (idUsuario)
);

CREATE TABLE TipoUsuario (
    idTipoUsuario int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (idTipoUsuario)
);

CREATE TABLE Marca (
    idMarca int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (idMarca)
);

CREATE TABLE ComprobantePago (
    idComprobante int(11) NOT NULL AUTO_INCREMENT, 
    idVenta int(11) NOT NULL, 
    montoTotal int(11) NOT NULL, 
    idTipoComprobante int(11) NOT NULL, 
    PRIMARY KEY (idComprobante)
);

CREATE TABLE Venta (
    idVenta int(11) NOT NULL AUTO_INCREMENT, 
    idCliente int(11) NOT NULL, 
    idCiudad int(11) NOT NULL, 
    subtotal decimal(9, 2) NOT NULL, 
    igv decimal(9, 2) NOT NULL, 
    descuento decimal(9, 2) NOT NULL, 
    fecha date NOT NULL, 
    hora time NOT NULL, 
    estado char(1) NOT NULL, 
    direccion varchar(50) NOT NULL, 
    PRIMARY KEY (idVenta)
);

CREATE TABLE Ciudad (
    idCiudad int(11) NOT NULL AUTO_INCREMENT, 
    idPais int(11) NOT NULL, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (idCiudad)
);

CREATE TABLE Pais (
    idPais int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (idPais)
);

CREATE TABLE Favoritos (
    idCliente int(11) NOT NULL, 
    idProducto int(11) NOT NULL, 
    PRIMARY KEY (idCliente, idProducto)
);

CREATE TABLE Detalle_venta (
    idDetVta int(11) NOT NULL, 
    idProducto int(11) NOT NULL, 
    idVenta int(11) NOT NULL, 
    cantidad int(11) NOT NULL, 
    precio decimal(9, 2) NOT NULL, 
    PRIMARY KEY (idDetVta, idProducto, idVenta)
);

CREATE TABLE Categoria (
    idCategoria int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (idCategoria)
);

CREATE TABLE CategoriaProducto (
    CategoriaidCategoria int(11) NOT NULL, 
    ProductoidProducto int(11) NOT NULL, 
    PRIMARY KEY (CategoriaidCategoria, ProductoidProducto)
);

CREATE TABLE Talla (
    id int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (id)
);

-- Se añade el campo imagen a la tabla Producto para almacenar la ruta de la imagen
CREATE TABLE Producto (
    idProducto int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    precio decimal(9, 2) NOT NULL, 
    stock int(11) NOT NULL, 
    idModelo int(11) NOT NULL, 
    idTalla int(11) NOT NULL, 
    imagen varchar(255) NULL,  -- Se añade el campo imagen para almacenar la ruta de la imagen
    PRIMARY KEY (idProducto)
);

CREATE TABLE Modelo (
    idModelo int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    idMarca int(11) NOT NULL, 
    PRIMARY KEY (idModelo)
);

CREATE TABLE nivelUsuario (
    idNivelUsuario int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    puntosRequeridos int(11) NOT NULL, 
    PRIMARY KEY (idNivelUsuario)
) comment='0-999 -> Hierro, 1000-2499 -> Bronce 5%, 2500-4999 -> Plata 7.5%, 5000-∞ -> Oro 10%';

CREATE TABLE tipoComprobante (
    idTipoComprobante int(11) NOT NULL AUTO_INCREMENT, 
    nombre varchar(50) NOT NULL, 
    PRIMARY KEY (idTipoComprobante)
);

-- Relación de claves foráneas
ALTER TABLE Reseña 
    ADD CONSTRAINT FKReseña738255 FOREIGN KEY (ClienteidCliente) REFERENCES Usuario (idUsuario),
    ADD CONSTRAINT FKReseña400882 FOREIGN KEY (ProductoidProducto) REFERENCES Producto (idProducto);

ALTER TABLE Usuario 
    ADD CONSTRAINT FKUsuario557876 FOREIGN KEY (idTipoUsuario) REFERENCES TipoUsuario (idTipoUsuario),
    ADD CONSTRAINT FKUsuario54363 FOREIGN KEY (idNivelUsuario) REFERENCES nivelUsuario (idNivelUsuario);

ALTER TABLE ComprobantePago 
    ADD CONSTRAINT FKComprobant934284 FOREIGN KEY (idVenta) REFERENCES Venta (idVenta),
    ADD CONSTRAINT FKComprobant835227 FOREIGN KEY (idTipoComprobante) REFERENCES tipoComprobante (idTipoComprobante);

ALTER TABLE Venta 
    ADD CONSTRAINT FKVenta832929 FOREIGN KEY (idCliente) REFERENCES Usuario (idUsuario),
    ADD CONSTRAINT FKVenta243636 FOREIGN KEY (idCiudad) REFERENCES Ciudad (idCiudad);

ALTER TABLE Ciudad 
    ADD CONSTRAINT FKCiudad961871 FOREIGN KEY (idPais) REFERENCES Pais (idPais);

ALTER TABLE Favoritos 
    ADD CONSTRAINT FKFavoritos21291 FOREIGN KEY (idCliente) REFERENCES Usuario (idUsuario),
    ADD CONSTRAINT FKFavoritos426683 FOREIGN KEY (idProducto) REFERENCES Producto (idProducto);

ALTER TABLE Detalle_venta 
    ADD CONSTRAINT FKDetalle_ve505603 FOREIGN KEY (idVenta) REFERENCES Venta (idVenta),
    ADD CONSTRAINT FKDetalle_ve347889 FOREIGN KEY (idProducto) REFERENCES Producto (idProducto);

ALTER TABLE CategoriaProducto 
    ADD CONSTRAINT FKCategoriaP322739 FOREIGN KEY (CategoriaidCategoria) REFERENCES Categoria (idCategoria),
    ADD CONSTRAINT FKCategoriaP106442 FOREIGN KEY (ProductoidProducto) REFERENCES Producto (idProducto);

ALTER TABLE Producto 
    ADD CONSTRAINT FKProducto553495 FOREIGN KEY (idTalla) REFERENCES Talla (id),
    ADD CONSTRAINT FKProducto919561 FOREIGN KEY (idModelo) REFERENCES Modelo (idModelo);

ALTER TABLE Modelo 
    ADD CONSTRAINT FKModelo452020 FOREIGN KEY (idMarca) REFERENCES Marca (idMarca);


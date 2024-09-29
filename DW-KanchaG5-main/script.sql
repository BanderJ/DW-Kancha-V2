--Para la creacion de la tabla me base en los campos que se piden en productos.json
create table producto (
    id int not null auto_increment,
    imagen varchar(255) not null,
    nombre varchar(100) not null,
    marca varchar(50) not null,
    precio decimal(10, 2) not null,
    preciokancha decimal(10, 2) not null,
    deporte varchar(50) not null,
    genero varchar(20) not null,
    color varchar(30) not null,
    tipo_producto varchar(50) not null,
    tipo varchar(50) not null,
    primary key (id)
);

--Inserciones para la tabla siguiendo la estructura planteada en productos.json

insert into producto (imagen, nombre, marca, precio, preciokancha, deporte, genero, color, tipo_producto, tipo) values 
('../img/foto (112).avif', 'f50 elite', 'adidas', 1709.90, 1679.90, 'fútbol', 'masculino', 'blanco', 'zapatillas', 'chimpunes');

insert into producto (imagen, nombre, marca, precio, preciokancha, deporte, genero, color, tipo_producto, tipo) values 
('../img/foto (27).avif', 'kd17 ''sunrise''', 'puma', 309.00, 289.00, 'fútbol', 'masculino', 'negro', 'zapatillas', 'chimpunes');

insert into producto (imagen, nombre, marca, precio, preciokancha, deporte, genero, color, tipo_producto, tipo) values 
('../img/foto (30).avif', 'kd1zxc7 ''sunrise''', 'puma', 309.00, 289.00, 'fútbol', 'masculino', 'rosado', 'zapatillas', 'chimpunes');

insert into producto (imagen, nombre, marca, precio, preciokancha, deporte, genero, color, tipo_producto, tipo) values 
('../img/foto (65).webp', 'mercurial superfly 9 elite', 'nike', 399.99, 399.99, 'fútbol', 'masculino', 'blanco', 'zapatillas', 'elite');

insert into producto (imagen, nombre, marca, precio, preciokancha, deporte, genero, color, tipo_producto, tipo) values 
('../img/foto (99).avif', 'kd17 ''sunrise''', 'nike', 309.00, 289.00, 'baloncesto', 'masculino', 'azul', 'zapatillas', 'elite');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha ,deporte ,genero ,color ,tipo_producto ,tipo) values 
('../img/foto (102).avif','kd1zxc7 ''sunrise''','adidas' ,309.00 ,289.00 ,'baloncesto','masculino','azul','zapatillas','elite');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha ,deporte ,genero ,color ,tipo_producto ,tipo) values 
('../img/foto(200).webp','gel-rocket 11 gunmetal','ascis' ,449.90 ,399.90 ,'voley','niño','negro','zapatillas','elite');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha ,deporte ,genero ,color ,tipo_producto ,tipo) values 
('../img/foto(201).avif','trae young unlimited 2 low','adidas' ,699.00 ,450.00 ,'básquet','masculino','azul','zapatillas','elite');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto(202).avif','jump man 23','adidas' ,309.00 ,289.00 ,'básquet','masculino','azul','zapatillas','elite');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (83).webp','mercurial vapor 7 jr.','nike' ,259.99 ,209.99 ,'básquet','niño','verde','zapatillas','cesped');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (80).webp','mercurial 7 jr.','nike' ,259.99 ,209.99 ,'fútbol','masculino','negro','zapatillas','cesped');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (77).webp','mercurial superfly 9 jr.','nike' ,299.99 ,239.99 ,'fútbol','masculino','verde','zapatillas','chimpunes');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (74).webp','mercurial 7 jr.','nike' ,299.99 ,239.99 ,'fútbol' ,'masculino' ,'rosado' ,'zapatillas' ,'chimpunes');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (68).webp','mercurial superfly 9 elite' ,'nike' ,399.99 ,339.99 ,'fútbol' ,'masculino' ,'rosado' ,'zapatillas' ,'chimpunes');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (71).webp','mercurial superfly 9 elite' ,'nike' ,399.99 ,339.99 ,'fútbol' ,'masculino' ,'amarillo' ,'zapatillas' ,'chimpunes');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (67).webp','mercurial superfly 9 elite' ,'nike' ,399.99 ,339.99 ,'fútbol' ,'masculino' ,'gris' ,'zapatillas' ,'chimpunes');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (24).avif','future 7 juniors fg/ag' ,'puma' ,219.99 ,151.99 ,'fútbol' ,'niño' ,'naranja' ,'zapatillas' ,'chimpunes');

insert into producto (imagen,nombre ,marca ,precio ,preciokancha,deporte,genero,color,tipo_producto,tipo) values 
('../img/foto (21).avif','future 7 juniors fg/ag ','puma' ,219.99 ,151.99 ,'fútbol' ,'masculino' ,'sonido' ,'zapatillas' ,'chimpunes');
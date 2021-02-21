-- Aquí se presentan todos los procedimientos que se crearon con el fin de realizar diferentes transacciones dentro de la base de datos.
-- Muchos de estos están relaciondos con la inserción, modificación y edición de datos. También para realizar operaciones dentro de las sesiones.

-- Creación de perfi en signup

delimiter $$

create procedure createProfile(
    in ced int,
    in nom varchar(50),
    in fec date,
    in sex varchar(1),
    in tel varchar(15),
    in pas varchar(150)
)
begin 
    insert into perfiles (cedula,nombre,fechaNacimiento,sexo,telefono,passhash) values (ced,nom,fec,sex,tel,pas);
end $$

delimiter ; 

-- Trae la información de usuario en sesión para mostrarla en la página de perfil

delimiter $$

create procedure getProfile(
    in ced int
)
begin 
    select cedula, nombre, fechaNacimiento, sexo, telefono, role from perfiles where cedula = ced;
end $$

delimiter ;

-- Actualizar todos los valores del perfil en la base de datos

delimiter $$

create procedure updateProfile(
    in ced int,
    in nom varchar(50),
    in fec date,
    in sex varchar(1),
    in tel varchar(15)
)
begin
    update perfiles set nombre = nom, fechaNacimiento = fec, sexo = sex, telefono = tel 
    where cedula = ced;
end $$

delimiter ;

-- Trae el rol del usuario actual

delimiter $$

create procedure getRole(
    in ced int
)
begin
    select role from perfiles where cedula = ced;
end $$

delimiter ;

-- Trae todos los perfiles sin rol  

delimiter $$

create procedure getRoleless(
)
begin
    select cedula, nombre, telefono, role from perfiles where role is null;
end $$

delimiter ;

-- Trae un único usuario para asignar rol

delimiter $$

create procedure getRolelessSearch(
    in ced int
)
begin
    select cedula, nombre, telefono, role from perfiles where cedula = ced;
end $$

delimiter ;

-- Da un rol al perfil seleccionado

delimiter $$

create procedure giveRole(
    in ced int,
    in rol varchar(15)
)
begin
    update perfiles set role = rol where cedula = ced;
end $$

delimiter ;

-- Insertar en la tabla correcta de rol (Médico, Enfermero, Administrativo, etc.)}


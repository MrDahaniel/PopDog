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
    insert into perfiles (cedula,nombre,fechaNacimiento,sexo,teléfono,passhash) values (ced,nom,fec,sex,tel,pas);
end $$

delimiter ;
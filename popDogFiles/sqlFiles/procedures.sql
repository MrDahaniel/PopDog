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

-- Trae a todos los perfiles en la base

delimiter $$

create procedure getAllProfiles(

)
begin
    select cedula, nombre, telefono, role from perfiles;
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

-- Trae de la base todas las especialidades registradas 

delimiter $$

create procedure getEspec(
)
begin
    select * from especialidad;
end $$

delimiter ;

-- Trae todos los horarios de la base de datos

delimiter $$

create procedure getSchedule(
)
begin
    select * from horario;
end $$ 

delimiter ;

-- Mega query para salvar el mundo (Y evitar doble registros)

delimiter $$

create procedure doubleChecker(
    in cedula int
)
begin
    select p.cedula, p.role from perfiles as p 
    left join medico as m on p.cedula = m.cedula
    left join enfermeras as e on p.cedula = e.cedula
    left join ingenieros as i on p.cedula = i.cedula
    left join serviciosGenerales as s on p.cedula = s.cedula
    left join administrativos as a on p.cedula = a.cedula
    left join pacientes as pa on p.cedula = pa.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae toda la info de un Administrativo

delimiter $$

create procedure getAdminProfile(
    in cedula int
)
begin 
    select * from perfiles as p 
    inner join administrativos as a on p.cedula = a.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae toda la info de un Médico

delimiter $$

create procedure getMedicProfile(
    in cedula int
)
begin
    select * from perfiles as p
    inner join medico as m on p.cedula = m.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae toda la info de una enfermera

delimiter $$

create procedure getNurseProfile(
    in cedula int
)
begin
    select * from perfiles as p
    inner join enfermeras as e on p.cedula = e.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae toda la info de ingeniero

delimiter $$

create procedure getEngieProfile(
    in cedula int
)
begin
    select * from perfiles as p
    inner join ingenieros as i on p.cedula = i.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae toda la info de alguien de servicios generales

delimiter $$

create procedure getSerGenProfile(
    in cedula int
)
begin
    select * from perfiles as p
    inner join serviciosGenerales as s on p.cedula = s.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae toda la info de un paciente

delimiter $$

create procedure getPatientProfile(
    in cedula int
)
begin
    select * from perfiles as p
    inner join pacientes as pa on p.cedula = pa.cedula
    where p.cedula = cedula;
end $$

delimiter ;

-- Trae un horarios de la base para mostrar los perfiles

delimiter $$

create procedure getSingleSchedule(
    in idHor int
)
begin
    select horaEntrada, horaSalida from horario where idHorario = idHor;
end $$

delimiter ;

-- Trae una especialidad para mostrar perfiles

delimiter $$

create procedure getSingleEspecial(
    in idEspecial int
)
begin
    select nombreEspecialidad from especialidad where idEspecialidad = idEspecial;
end $$

delimiter ;

-- Trae la ubicación a partir de un id

delimiter $$

create procedure getLocation(
    in idUbi int
)
begin
    select s.nombreSector, tu.nombreTipUbi, u.nombreUbi from ubicacion as u 
    inner join sector as s on u.idSector = s.idSector
    inner join tipoUbicacion as tu on u.idTipUbi = tu.idTipUbi 
    where u.idUbicacion = idUbi;
end $$

delimiter ;
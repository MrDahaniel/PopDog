--Este script existe con el fin de mantener consistentes las tablas entre las diferentes personas 
--Lo ideal sería tener una base de datos hosteada pero dudo que podamos hacer eso lol

create database popdogdb;

use popdogdb;

create table perfiles(
    cedula int primary key, 
    nombre varchar(50) not null,
    fechaNacimiento date,
    sexo varchar(1) not null,
    telefono varchar(15),
    passhash varchar(150),
    role varchar(20)
);

create table horario(
    idHorario serial primary key,
    horaEntrada time not null,
    horaSalida time not null
);

create table sector(
    idSector serial primary key,
    nombreSector varchar(150)
);

create table tipoUbicacion(
    idTipUbi serial primary key,
    nombreTipUbi varchar(150)
);

create table ubicacion(
    idUbicacion serial primary key,
    idTipUbi int references tipoUbicacion(idTipUbi),
    idSector int references sector(idSector),
    nombreUbi varchar(150) not null
);

create table especialidad(
    idEspecialidad serial primary key, 
    nombreEspecialidad varchar(100) not null
);

create table medico(
    idMedico serial primary key, 
    cedula int references perfiles(cedula),
    idEspecialidad int references especialidad(idEspecialidad),
    idHorario int references horario(idHorario)
);

create table enfermeras(
    idEnfermera serial primary key,
    cedula int references perfiles(cedula),
    idHorario int references horario(idHorario),
    idUbicacion int references ubicacion(idUbicacion)
);

create table serviciosGenerales(
    idSerGen serial primary key,
    cedula int references perfiles(cedula),
    idHorario int references horario(idHorario)
);

create table tipoServicio(
    idTipSer serial primary key,
    nombreServicio varchar(150)
);

create table ingenieros(
    idIngeniero serial primary key, 
    cedula int references perfiles(cedula),
    idHorario int references horario(idHorario)
);

create table tipoEquipo(
    idTipEqu serial primary key, 
    nombreTipEqu varchar(50)
);

create table equipo(
    idEquipo serial primary key, 
    idUbicacion int references ubicacion(idUbicacion),
    idTipEqu int references tipoEquipo(idTipEqu)
);

create table ordenMantenimiento(
    idOrdenMantenimiento serial primary key,
    idEquipo int references equipo(idEquipo),
    idIngeniero int references ingenieros(idIngeniero),
    ordenCompletada boolean default false
);

create table proveedores(
    idProveedor serial primary key,
    nombre varchar(50) not null,
    direccion varchar(150) not null
);

create table administrativos(
    idAdministrativo serial primary key,
    cedula int references perfiles(cedula),
    idHorario int references horario(idHorario),
    areaAsig varchar(150)
);

create table item(
    idItem serial primary key,
    idProveedor int references proveedores(idProveedor),
    nombre varchar(150),
    cantidad int
);

create table Pedidos(
    idPedido serial primary key,
    idItem int references item(idItem),
    idAdministrativo int references administrativos(idAdministrativo),
    cantidad int not null, 
    fecha date 
);

create table EPS(
    idEPS serial primary key,
    nombreEPS varchar(50)
);

create table historialMedico(
    idHistorial int primary key,
    fechaSubida date not null,
    documento blob 
);

create table pacientes(
    idPaciente serial primary key,
    cedula int references perfiles(cedula),
    idUbicacion int references ubicacion(idUbicacion),
    idEPS int references EPS(idEPS),
    idHistorial int references historialMedico(idHistorial),
    peso float
);

create table medioEntrada(
    idMedio serial primary key,
    nombreMedio varchar(150)
);

create table ingresos(
    idIngreso serial primary key,
    idPaciente int references pacientes(idPaciente),
    idMedio int references medioEntrada(idMedio),
    fecha date,
    hora time, 
    estado boolean default false
);

create table salidas(
    idSalidas serial primary key, 
    idPaciente int references pacientes(idPaciente),
    idMedicoAut int references medico(idMedico),
    fecha date,
    hora time
);
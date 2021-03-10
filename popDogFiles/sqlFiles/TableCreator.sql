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
    idTipUbi BIGINT UNSIGNED, foreign key(idTipUbi) references tipoUbicacion(idTipUbi),
    idSector BIGINT UNSIGNED, foreign key(idSector) references sector(idSector),
    nombreUbi varchar(150) not null
);

create table especialidad(
    idEspecialidad serial primary key, 
    nombreEspecialidad varchar(100) not null
);

create table medico(
    idMedico serial primary key, 
    cedula int, foreign key(cedula) references perfiles(cedula),
    idEspecialidad BIGINT UNSIGNED, foreign key(idEspecialidad) references especialidad(idEspecialidad),
    idHorario BIGINT UNSIGNED, foreign key(idHorario) references horario(idHorario)
);

create table enfermeras(
    idEnfermera serial primary key,
    cedula int, foreign key(cedula) references perfiles(cedula),
    idHorario BIGINT UNSIGNED, foreign key(idHorario) references horario(idHorario),
    idUbicacion BIGINT UNSIGNED, foreign key(idUbicacion) references ubicacion(idUbicacion)
);

create table serviciosGenerales(
    idSerGen serial primary key,
    cedula int, foreign key(cedula) references perfiles(cedula),
    idHorario BIGINT UNSIGNED, foreign key(idHorario) references horario(idHorario)
);

create table tipoServicio(
    idTipSer serial primary key,
    nombreServicio varchar(150)
);

create table ingenieros(
    idIngeniero serial primary key, 
    cedula int, foreign key(cedula) references perfiles(cedula),
    idHorario BIGINT UNSIGNED, foreign key(idHorario) references horario(idHorario)
);

create table tipoEquipo(
    idTipEqu serial primary key, 
    nombreTipEqu varchar(50)
);

create table equipo(
    idEquipo serial primary key, 
    idUbicacion BIGINT UNSIGNED, foreign key(idUbicacion) references ubicacion(idUbicacion),
    idTipEqu BIGINT UNSIGNED, foreign key(idTipEqu) references tipoEquipo(idTipEqu)
);

create table ordenMantenimiento(
    idOrdenMantenimiento serial primary key,
    idEquipo BIGINT UNSIGNED, foreign key(idEquipo) references equipo(idEquipo),
    idIngeniero BIGINT UNSIGNED, foreign key(idIngeniero) references ingenieros(idIngeniero),
    ordenCompletada boolean default false
);

create table proveedores(
    idProveedor serial primary key,
    nombre varchar(50) not null,
    direccion varchar(150) not null
);

create table administrativos(
    idAdministrativo serial primary key,
    cedula int, foreign key(cedula) references perfiles(cedula),
    idHorario BIGINT UNSIGNED, foreign key(idHorario) references horario(idHorario),
    areaAsig varchar(150)
);

create table item(
    idItem serial primary key,
    idProveedor BIGINT UNSIGNED, foreign key(idProveedor) references proveedores(idProveedor),
    nombre varchar(150),
    cantidad int
);

create table Pedidos(
    idPedido serial primary key,
    idItem BIGINT UNSIGNED, foreign key(idItem) references item(idItem),
    idAdministrativo BIGINT UNSIGNED, foreign key(idAdministrativo) references administrativos(idAdministrativo),
    cantidad int not null, 
    fecha date 
);

create table EPS(
    idEPS serial primary key,
    nombreEPS varchar(50)
);

create table historialMedico(
    idHistorial serial primary key,
    fechaSubida date not null,
    documento blob 
);

create table pacientes(
    idPaciente serial primary key,
    cedula int, foreign key(cedula) references perfiles(cedula),
    idUbicacion BIGINT UNSIGNED, foreign key(idUbicacion) references ubicacion(idUbicacion),
    idEPS BIGINT UNSIGNED, foreign key(idEPS) references EPS(idEPS),
    idHistorial BIGINT UNSIGNED references historialMedico(idHistorial),
    peso float
);

create table medioEntrada(
    idMedio serial primary key,
    nombreMedio varchar(150)
);

create table ingresos(
    idIngreso serial primary key,
    idPaciente BIGINT UNSIGNED, foreign key(idPaciente) references pacientes(idPaciente),
    idMedio BIGINT UNSIGNED, foreign key(idMedio) references medioEntrada(idMedio),
    fecha date,
    hora time, 
    estado boolean default false
);

create table salidas(
    idSalidas serial primary key, 
    idPaciente BIGINT UNSIGNED, foreign key(idPaciente) references pacientes(idPaciente),
    idMedicoAut BIGINT UNSIGNED, foreign key(idMedicoAut) references medico(idMedico),
    fecha date,
    hora time
);

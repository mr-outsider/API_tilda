-- Tabla: colegios
CREATE TABLE colegios (
    id VARCHAR(36) PRIMARY KEY,
    clave_cct VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    nivel_educativo VARCHAR(50) NOT NULL,
    calle VARCHAR(255) NOT NULL,
    colonia VARCHAR(255) NOT NULL,
    municipio VARCHAR(100) NOT NULL,
    estado VARCHAR(100) NOT NULL,
    codigo_postal VARCHAR(10) NOT NULL,
    latitud DECIMAL(9,6),
    longitud DECIMAL(9,6),
    telefono VARCHAR(20),
    correo_electronico VARCHAR(100) UNIQUE NOT NULL,
    nombre_director VARCHAR(255) NOT NULL,
    turno VARCHAR(20) NOT NULL,
    estatus VARCHAR(20) NOT NULL
);

-- Tabla: estudiantes
CREATE TABLE estudiantes (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    genero VARCHAR(20) NOT NULL,
    curp VARCHAR(18) UNIQUE NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    grado_escolar VARCHAR(50) NOT NULL,
    especialidad VARCHAR(255),
    promedio_general DECIMAL(4,2), -- Ajustado para permitir promedios como 9.75
    carrera VARCHAR(150),
    id_escuela VARCHAR(36) REFERENCES colegios(id) ON DELETE CASCADE
);

-- Tabla: facturas
CREATE TABLE facturas (
    id VARCHAR(36) PRIMARY KEY,
    fecha_emision DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    monto_pagado DECIMAL(10,2) DEFAULT 0.00 NOT NULL,
    estatus VARCHAR(20) DEFAULT 'pendiente' NOT NULL,
    id_estudiante VARCHAR(36) REFERENCES estudiantes(id) ON DELETE CASCADE
);

-- Tabla: pagos
CREATE TABLE pagos (
    id VARCHAR(36) PRIMARY KEY,
    fecha_pago DATE NOT NULL,
    monto_pagado DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    referencia_pago VARCHAR(70) NOT NULL,
    cuenta_beneficiaria VARCHAR(25) NOT NULL,
    institucion_emisora VARCHAR(100),
    institucion_receptora VARCHAR(100) NOT NULL,
    id_factura VARCHAR(36) REFERENCES facturas(id) ON DELETE CASCADE
);

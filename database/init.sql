-- Crear base de datos para la veterinaria
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mascotas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(100),
    edad INTEGER,
    peso DECIMAL(5,2),
    cliente_id INTEGER REFERENCES clientes(id) ON DELETE CASCADE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS citas (
    id SERIAL PRIMARY KEY,
    mascota_id INTEGER REFERENCES mascotas(id) ON DELETE CASCADE,
    fecha_cita TIMESTAMP NOT NULL,
    motivo TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    observaciones TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS historial_medico (
    id SERIAL PRIMARY KEY,
    mascota_id INTEGER REFERENCES mascotas(id) ON DELETE CASCADE,
    fecha_consulta TIMESTAMP NOT NULL,
    diagnostico TEXT NOT NULL,
    tratamiento TEXT,
    medicamentos TEXT,
    veterinario VARCHAR(100),
    proxima_cita DATE
);

-- Insertar datos de ejemplo
INSERT INTO clientes (nombre, apellido, telefono, email, direccion) VALUES
('Juan', 'Pérez', '555-0101', 'juan.perez@email.com', 'Calle Principal 123'),
('María', 'González', '555-0102', 'maria.gonzalez@email.com', 'Avenida Central 456'),
('Carlos', 'Rodríguez', '555-0103', 'carlos.rodriguez@email.com', 'Plaza Mayor 789');

INSERT INTO mascotas (nombre, especie, raza, edad, peso, cliente_id) VALUES
('Max', 'Perro', 'Labrador', 3, 30.5, 1),
('Luna', 'Gato', 'Persa', 2, 4.2, 1),
('Rocky', 'Perro', 'Pastor Alemán', 5, 35.0, 2),
('Michi', 'Gato', 'Siamés', 1, 3.5, 3);

INSERT INTO citas (mascota_id, fecha_cita, motivo, estado) VALUES
(1, '2025-11-20 10:00:00', 'Vacunación anual', 'Pendiente'),
(2, '2025-11-22 15:30:00', 'Revisión general', 'Pendiente'),
(3, '2025-11-25 11:00:00', 'Control de peso', 'Pendiente');

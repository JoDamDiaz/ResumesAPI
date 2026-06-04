SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS resumes_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE resumes_db;

-- ── Tabla principal de usuarios ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id   INT          NOT NULL AUTO_INCREMENT,
    nombre    VARCHAR(255) NOT NULL,
    telefono  VARCHAR(20)  NULL,
    correo    VARCHAR(255) NOT NULL,
    linkedin  VARCHAR(255) NULL,
    github    VARCHAR(255) NULL,
    ubicacion VARCHAR(255) NULL,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Una fila por empleo (normalización: 1 user → N experiencias) ──────────────
CREATE TABLE IF NOT EXISTS experiencia_user (
    id            INT          NOT NULL AUTO_INCREMENT,
    user_id       INT          NOT NULL,
    cargo         VARCHAR(255) NOT NULL,
    empresa       VARCHAR(255) NOT NULL,
    tiempo_inicio DATE         NOT NULL,
    tiempo_final  DATE         NULL,      -- NULL = empleo actual
    PRIMARY KEY (id),
    CONSTRAINT fk_exp_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Una fila por función (normalización: 1 experiencia → N funciones) ─────────
CREATE TABLE IF NOT EXISTS funcion_experiencia (
    id             INT  NOT NULL AUTO_INCREMENT,
    experiencia_id INT  NOT NULL,
    descripcion    TEXT NOT NULL,
    orden          INT  NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    CONSTRAINT fk_funcion_exp FOREIGN KEY (experiencia_id)
        REFERENCES experiencia_user (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ── Datos de prueba ────────────────────────────────────────────────────────────
INSERT INTO users (nombre, telefono, correo, linkedin, github, ubicacion) VALUES
('Ana García López',     '+52 55 1234 5678', 'ana.garcia@ejemplo.com',     'linkedin.com/in/anagarcia',     'github.com/anagarcia',     'Ciudad de México, MX'),
('Carlos Mendoza Ruiz',  '+52 33 9876 5432', 'carlos.mendoza@ejemplo.com',  'linkedin.com/in/carlosmendoza', 'github.com/carlosmendoza', 'Guadalajara, MX'),
('Laura Jiménez Torres', '+52 81 5555 0001', 'laura.jimenez@ejemplo.com',   'linkedin.com/in/laurajimenez',  'github.com/laurajimenez',  'Monterrey, MX');

-- Ana García – 3 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(1, 'Desarrolladora Backend Senior', 'TechCorp MX',    '2022-03-01', NULL),
(1, 'Desarrolladora Backend',        'Startup Digital', '2020-01-01', '2022-02-28'),
(1, 'Trainee Backend',               'Agencia Web',     '2019-06-01', '2019-12-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(1, 'Diseño e implementación de microservicios con FastAPI y Python', 1),
(1, 'Optimización de queries en MySQL reduciendo tiempos de respuesta en 40%', 2),
(1, 'Liderazgo técnico de equipo de 4 desarrolladores', 3),
(2, 'Desarrollo de APIs REST con Django Rest Framework', 1),
(2, 'Integración con servicios de pago (Stripe, Conekta)', 2),
(2, 'Automatización de pruebas unitarias con pytest', 3),
(3, 'Apoyo en mantenimiento de aplicaciones web con Flask', 1),
(3, 'Documentación técnica de endpoints', 2);

-- Carlos Mendoza – 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(2, 'Ingeniero de Software Full Stack', 'Fintech MX',        '2021-07-01', NULL),
(2, 'Desarrollador Frontend',           'Consultora Digital', '2019-09-01', '2021-06-30');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(4, 'Desarrollo de módulos frontend con React y TypeScript', 1),
(4, 'Construcción de servicios backend con Node.js y Express', 2),
(4, 'Implementación de autenticación con OAuth 2.0 y JWT', 3),
(5, 'Creación de interfaces de usuario con Vue.js', 1),
(5, 'Consumo de APIs REST y manejo de estado con Vuex', 2),
(5, 'Optimización de rendimiento web (Lighthouse score +90)', 3);

-- Laura Jiménez – 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(3, 'Data Engineer',    'Retail Analytics',  '2023-01-01', NULL),
(3, 'Analista de Datos','Empresa Logística', '2020-08-01', '2022-12-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(6, 'Diseño de pipelines de datos con Apache Airflow', 1),
(6, 'Modelado dimensional en Redshift y BigQuery', 2),
(6, 'Automatización de reportes en Power BI via API', 3),
(7, 'Análisis exploratorio de datos con pandas y numpy', 1),
(7, 'Creación de dashboards en Tableau para equipos comerciales', 2),
(7, 'Limpieza y transformación de datasets de +5M filas', 3);

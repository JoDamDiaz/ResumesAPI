SET NAMES utf8mb4;
CREATE DATABASE IF NOT EXISTS resumes_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE resumes_db;

-- ── Roles ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS roles (
    role_id INT          NOT NULL AUTO_INCREMENT,
    nombre  VARCHAR(50)  NOT NULL,
    PRIMARY KEY (role_id),
    UNIQUE KEY uq_roles_nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO roles (role_id, nombre) VALUES
(1, 'admin'),
(2, 'auditor'),
(3, 'usuario');

-- ── Tabla principal de usuarios ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id   INT          NOT NULL AUTO_INCREMENT,
    nombre    VARCHAR(255) NOT NULL,
    telefono  VARCHAR(20)  NULL,
    correo    VARCHAR(255) NOT NULL,
    linkedin  VARCHAR(255) NULL,
    github    VARCHAR(255) NULL,
    ubicacion        VARCHAR(255) NULL,
    hashed_password  VARCHAR(255) NULL,
    is_active        TINYINT(1)   NOT NULL DEFAULT 1,
    role_id          INT          NOT NULL DEFAULT 3,
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_users_correo (correo),
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles (role_id)
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

-- ── Datos de prueba (role_id DEFAULT 3 = usuario) ─────────────────────────────
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

-- ── Usuarios 4-13 (datos dummy adicionales) ───────────────────────────────────
INSERT INTO users (nombre, telefono, correo, linkedin, github, ubicacion) VALUES
('Miguel Rodríguez Soto',   '+52 55 2200 3344', 'miguel.rodriguez@ejemplo.com',  'linkedin.com/in/miguelrodriguez', 'github.com/miguelrodriguez', 'Ciudad de México, MX'),
('Sofía Herrera Blanco',    '+52 33 4400 5566', 'sofia.herrera@ejemplo.com',      'linkedin.com/in/sofiaherrera',    'github.com/sofiaherrera',   'Guadalajara, MX'),
('Roberto Castillo Vega',   '+52 81 6600 7788', 'roberto.castillo@ejemplo.com',   'linkedin.com/in/robertocastillo', 'github.com/rcastillo',      'Monterrey, MX'),
('Valentina Cruz Peña',     '+52 55 8800 9900', 'valentina.cruz@ejemplo.com',     'linkedin.com/in/valentinacruz',   NULL,                        'Ciudad de México, MX'),
('Diego Morales Fuentes',   '+52 22 1122 3344', 'diego.morales@ejemplo.com',      'linkedin.com/in/diegomorales',    'github.com/diegomorales',   'Puebla, MX'),
('Paola Reyes Gutiérrez',   '+52 55 5544 6677', 'paola.reyes@ejemplo.com',        'linkedin.com/in/paolareyes',      'github.com/paolareyes',     'Ciudad de México, MX'),
('Andrés Vega Salinas',     '+52 33 7788 9900', 'andres.vega@ejemplo.com',        'linkedin.com/in/andresvega',      'github.com/andresvega',     'Guadalajara, MX'),
('Mariana López Ibáñez',    '+52 81 2233 4455', 'mariana.lopez@ejemplo.com',      'linkedin.com/in/marianalopez',    'github.com/marianalopez',   'Monterrey, MX'),
('Fernando Sánchez Ortega', '+52 55 6677 8899', 'fernando.sanchez@ejemplo.com',   'linkedin.com/in/fernandosanchez', 'github.com/fsanchez',       'Ciudad de México, MX'),
('Isabella Díaz Ramírez',   '+52 33 9900 1122', 'isabella.diaz@ejemplo.com',      'linkedin.com/in/isabelladiaz',    NULL,                        'Guadalajara, MX');

-- Miguel Rodríguez (user 4) – DevOps: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(4, 'DevOps Engineer Senior', 'CloudTech MX',   '2021-06-01', NULL),
(4, 'Administrador de Sistemas', 'Hosting MX',  '2018-03-01', '2021-05-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(8,  'Diseño y mantenimiento de pipelines CI/CD con GitHub Actions y Jenkins', 1),
(8,  'Orquestación de contenedores con Kubernetes y Helm en GCP', 2),
(8,  'Reducción del tiempo de despliegue en un 60% mediante automatización', 3),
(9,  'Administración de servidores Linux (Ubuntu/CentOS) on-premise', 1),
(9,  'Implementación de monitoreo con Zabbix y Grafana', 2),
(9,  'Gestión de backups y planes de recuperación ante desastres', 3);

-- Sofía Herrera (user 5) – UX/UI Design: 3 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(5, 'UX Lead',         'Agencia Creativa MX', '2022-09-01', NULL),
(5, 'UX/UI Designer',  'App Factory',         '2020-02-01', '2022-08-31'),
(5, 'Diseñadora Junior','Studio Digital',      '2019-01-01', '2020-01-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(10, 'Definición de estrategia de diseño centrada en el usuario para productos B2C', 1),
(10, 'Liderazgo de sesiones de design thinking y pruebas de usabilidad', 2),
(10, 'Construcción del design system compartido con el equipo de frontend', 3),
(11, 'Creación de wireframes, prototipos y flujos de usuario en Figma', 1),
(11, 'Realización de entrevistas y pruebas A/B con usuarios reales', 2),
(11, 'Entrega de especificaciones de diseño al equipo de desarrollo', 3),
(12, 'Diseño de pantallas e íconos para aplicaciones móviles iOS y Android', 1),
(12, 'Apoyo en la identidad visual y branding de clientes startup', 2);

-- Roberto Castillo (user 6) – Mobile: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(6, 'Mobile Developer Senior', 'AppMX',        '2021-01-01', NULL),
(6, 'iOS Developer',           'StartupMóvil', '2018-06-01', '2020-12-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(13, 'Desarrollo de aplicaciones multiplataforma con React Native y Expo', 1),
(13, 'Integración con APIs REST y WebSockets para funciones en tiempo real', 2),
(13, 'Publicación y gestión de releases en App Store y Google Play', 3),
(14, 'Desarrollo nativo iOS con Swift y SwiftUI', 1),
(14, 'Integración con servicios de Apple: Sign In, Push Notifications, StoreKit', 2),
(14, 'Reducción del crash rate de 2.1% a 0.3% en producción', 3);

-- Valentina Cruz (user 7) – Product Manager: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(7, 'Product Manager',     'Ecommerce MX',    '2022-01-01', NULL),
(7, 'Project Coordinator', 'Consultora Tech', '2019-05-01', '2021-12-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(15, 'Definición y priorización del roadmap del producto con stakeholders', 1),
(15, 'Gestión de backlogs en Jira y coordinación de sprints con equipos ágiles', 2),
(15, 'Incremento de conversión del sitio en 35% mediante experimentos controlados', 3),
(16, 'Coordinación de proyectos de transformación digital para 3 clientes simultáneos', 1),
(16, 'Elaboración de reportes de avance y gestión de riesgos en MS Project', 2),
(16, 'Facilitación de retrospectivas y ceremonias Scrum', 3);

-- Diego Morales (user 8) – Cybersecurity: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(8, 'Analista de Seguridad Informática', 'BancoTech MX', '2023-03-01', NULL),
(8, 'Pentester Junior',                  'SecureIT MX',  '2020-08-01', '2023-02-28');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(17, 'Análisis y respuesta a incidentes de seguridad en infraestructura bancaria', 1),
(17, 'Implementación de políticas de seguridad bajo estándar PCI-DSS', 2),
(17, 'Monitoreo continuo con SIEM (Splunk) y gestión de vulnerabilidades', 3),
(18, 'Ejecución de pruebas de penetración en aplicaciones web y redes internas', 1),
(18, 'Elaboración de reportes de vulnerabilidades con CVSS scoring', 2),
(18, 'Capacitación en phishing awareness para equipos no técnicos', 3);

-- Paola Reyes (user 9) – ML Engineer: 3 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(9, 'ML Engineer',         'AI Labs MX',    '2022-06-01', NULL),
(9, 'Data Scientist',      'Analytics Corp','2019-09-01', '2022-05-31'),
(9, 'Research Assistant',  'UNAM',          '2018-01-01', '2019-08-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(19, 'Entrenamiento y despliegue de modelos NLP con Hugging Face y FastAPI', 1),
(19, 'Construcción de feature stores con Feast y pipelines MLOps con MLflow', 2),
(19, 'Reducción de latencia de inferencia de 800ms a 120ms con TorchScript', 3),
(20, 'Desarrollo de modelos de predicción de churn con XGBoost y SHAP', 1),
(20, 'Análisis estadístico y visualización con seaborn, Plotly y Streamlit', 2),
(20, 'Presentación de hallazgos de datos a audiencias ejecutivas', 3),
(21, 'Investigación en procesamiento de lenguaje natural para tesis de maestría', 1),
(21, 'Publicación de paper en congreso nacional de inteligencia artificial', 2);

-- Andrés Vega (user 10) – Cloud Architect: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(10, 'Cloud Architect',        'AWS Partner MX', '2021-03-01', NULL),
(10, 'Infrastructure Engineer','Telecom MX',     '2017-07-01', '2021-02-28');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(22, 'Diseño de arquitecturas multi-cuenta en AWS con Landing Zone y Control Tower', 1),
(22, 'Implementación de infraestructura como código con Terraform y CDK', 2),
(22, 'Optimización de costos cloud logrando ahorro anual de $200k USD', 3),
(23, 'Gestión de red MPLS y migración de datacenter on-premise a AWS', 1),
(23, 'Automatización de aprovisionamiento con Ansible y Chef', 2),
(23, 'Disponibilidad de servicios críticos mantenida en 99.97%', 3);

-- Mariana López (user 11) – QA Engineer: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(11, 'QA Automation Lead', 'Fintech QRO',   '2022-04-01', NULL),
(11, 'QA Manual Tester',   'Software House','2019-11-01', '2022-03-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(24, 'Diseño del framework de automatización E2E con Playwright y TypeScript', 1),
(24, 'Integración de pruebas automatizadas en pipeline CI/CD reduciendo bugs en producción 70%', 2),
(24, 'Definición de estrategia de testing: unitario, integración, contrato y carga', 3),
(25, 'Ejecución de casos de prueba funcionales y regresión en aplicaciones web', 1),
(25, 'Documentación de bugs en Jira con evidencia y pasos de reproducción', 2),
(25, 'Apoyo en pruebas de aceptación de usuario (UAT) con clientes finales', 3);

-- Fernando Sánchez (user 12) – DBA: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(12, 'DBA Senior',  'Retail Nacional', '2020-01-01', NULL),
(12, 'DBA Junior',  'ERP Solutions',   '2016-03-01', '2019-12-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(26, 'Administración de instancias MySQL, PostgreSQL y Oracle en producción', 1),
(26, 'Tuning de consultas críticas reduciendo tiempos de respuesta hasta 80%', 2),
(26, 'Diseño e implementación de estrategia de alta disponibilidad con réplicas', 3),
(27, 'Mantenimiento de bases de datos ERP (SAP B1) para clientes PYME', 1),
(27, 'Generación de reportes y vistas para módulos de finanzas e inventario', 2),
(27, 'Migración de datos entre versiones de SAP con validación de integridad', 3);

-- Isabella Díaz (user 13) – Scrum Master: 2 empleos
INSERT INTO experiencia_user (user_id, cargo, empresa, tiempo_inicio, tiempo_final) VALUES
(13, 'Scrum Master',  'Tech Consulting MX', '2021-09-01', NULL),
(13, 'Agile Coach',   'Digital Agency',     '2018-04-01', '2021-08-31');

INSERT INTO funcion_experiencia (experiencia_id, descripcion, orden) VALUES
(28, 'Facilitación de ceremonias Scrum para 4 equipos de desarrollo simultáneos', 1),
(28, 'Eliminación de impedimentos organizacionales y mejora de velocity en 45%', 2),
(28, 'Coaching a Product Owners en refinamiento y priorización de backlog', 3),
(29, 'Implementación de marcos ágiles (Scrum, Kanban, SAFe) en empresas medianas', 1),
(29, 'Capacitación de más de 150 colaboradores en prácticas ágiles', 2),
(29, 'Diseño de métricas de madurez ágil y seguimiento trimestral con dirección', 3);

-- ── Credenciales y roles de usuarios de prueba ────────────────────────────────
-- Roles: 1=admin  2=auditor  3=usuario (default)
-- Patrón de contraseñas: <Nombre>1234!
UPDATE users SET hashed_password = '$2b$12$61FVcAa9g52pC/WU5H.gHOTVpGYOGwW2ekHNd3fBQ2EziJWgAhe62', role_id = 1 WHERE correo = 'ana.garcia@ejemplo.com';      -- Ana1234!       admin
UPDATE users SET hashed_password = '$2b$12$ieuqW/wWfw/r6cmgqmn4XOJD.XL/LN3vXjTfNo1NXM56XJwKJG08y', role_id = 2 WHERE correo = 'carlos.mendoza@ejemplo.com';   -- Carlos1234!    auditor
UPDATE users SET hashed_password = '$2b$12$VpK3MyW037Pfh36P6X6gDOIvMXXJa.5J9bBUbRvyNSO025CeR4eZu', role_id = 3 WHERE correo = 'laura.jimenez@ejemplo.com';    -- Laura1234!     usuario
UPDATE users SET hashed_password = '$2b$12$tAwhfJacx/lgoJHHhjFMBOlrYo2harsWDDdoVn3lEz6QeF.q9LL0K', role_id = 3 WHERE correo = 'miguel.rodriguez@ejemplo.com'; -- Miguel1234!    usuario
UPDATE users SET hashed_password = '$2b$12$/VcDJz9Ln0/KmIc8IFIE9OGHzf4fvf2oA.AUc15.bK55fUZr3isvG', role_id = 2 WHERE correo = 'sofia.herrera@ejemplo.com';    -- Sofia1234!     auditor
UPDATE users SET hashed_password = '$2b$12$vKW7AplItSdWRveg25L9k.6xxOi6cwNcSNUAqYJPvInBe952OSCSq', role_id = 3 WHERE correo = 'roberto.castillo@ejemplo.com'; -- Roberto1234!   usuario
UPDATE users SET hashed_password = '$2b$12$ZRwab4g8vlA7fywZaflqf..rOqkgPwK.dUcDdHcopuritU5nF67ue', role_id = 1 WHERE correo = 'valentina.cruz@ejemplo.com';   -- Valentina1234! admin
UPDATE users SET hashed_password = '$2b$12$AcdiWCn1X7Klt1aM.gKlAeM/B93nwSdvs3I6/q4eJT0TQvaeKGLp.', role_id = 3 WHERE correo = 'diego.morales@ejemplo.com';   -- Diego1234!     usuario
UPDATE users SET hashed_password = '$2b$12$0h/jhmvA6svEO7dJmRAurOubmb78Ot7lG2OAQHtjQBzAk0FHHqPV.',  role_id = 3 WHERE correo = 'paola.reyes@ejemplo.com';     -- Paola1234!     usuario
UPDATE users SET hashed_password = '$2b$12$g7mkOavkpGbctLgxhEqM6OmehEUWjZKNSBnZIRza/va8vryUA4uqK', role_id = 2 WHERE correo = 'andres.vega@ejemplo.com';      -- Andres1234!    auditor
UPDATE users SET hashed_password = '$2b$12$lid/ZitBP8T19COmxHTQYeHmOEHFQuNpNfMgMlcfqmqkbUx1HWzO.', role_id = 3 WHERE correo = 'mariana.lopez@ejemplo.com';   -- Mariana1234!   usuario
UPDATE users SET hashed_password = '$2b$12$0BJJZxx2jgz4M9ag7y121OiyytnRibT0z7v18H8/Br92AFD8fQKSO', role_id = 2 WHERE correo = 'fernando.sanchez@ejemplo.com'; -- Fernando1234!  auditor
UPDATE users SET hashed_password = '$2b$12$GeYU/KS8zscMt63x1rQukuhWAw4A8YrV5cUqpRPLBs23vcdusBc6u', role_id = 3 WHERE correo = 'isabella.diaz@ejemplo.com';   -- Isabella1234!  usuario

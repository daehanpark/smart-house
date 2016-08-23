DROP DATABASE IF EXISTS smarthouse;

CREATE DATABASE IF NOT EXISTS smarthouse;

CREATE TABLE IF NOT EXISTS smarthouse.atributos (
id int(11) PRIMARY KEY AUTO_INCREMENT,
nombre_dispositivo varchar(32) NOT NULL,
nombre_atributo varchar(32) NOT NULL,
UNIQUE KEY dispo_atrib (nombre_dispositivo,nombre_atributo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS smarthouse.preferencias (
id int(11) PRIMARY KEY AUTO_INCREMENT,
id_atributo int(11) NOT NULL,
valor varchar(16) NOT NULL,
hora int(11) NOT NULL,
dia varchar(16) NOT NULL,
FOREIGN KEY (id_atributo) REFERENCES smarthouse.atributos (id) ON DELETE CASCADE,
UNIQUE KEY preferencia (id_atributo,valor,hora,dia)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS smarthouse.usuarios (
id int(11) PRIMARY KEY AUTO_INCREMENT,
nombre varchar(32) NOT NULL,
UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS smarthouse.usuarios_preferencias (
id_usuario int(11) NOT NULL,
id_preferencia int(11) NOT NULL,
popularidad int(11) NOT NULL DEFAULT 1,
PRIMARY KEY(id_usuario,id_preferencia),
FOREIGN KEY (id_usuario) REFERENCES smarthouse.usuarios (id) ON DELETE CASCADE,
FOREIGN KEY (id_preferencia) REFERENCES smarthouse.preferencias (id) ON DELETE CASCADE,
CHECK (popularidad>=0)
)ENGINE=InnoDB;

CREATE OR REPLACE VIEW smarthouse.v_preferencia AS
SELECT P.id,A.nombre_dispositivo,A.nombre_atributo,P.valor,P.hora,P.dia
FROM smarthouse.preferencias P, smarthouse.atributos A
WHERE P.id_atributo=A.id;

CREATE OR REPLACE VIEW smarthouse.v_preferencia_usuarios AS
SELECT U.id as id_usuario, P.id as id_preferencia, U.nombre as nombre_usuario, A.nombre_dispositivo,A.nombre_atributo,P.valor,P.hora,P.dia, UP.popularidad
FROM smarthouse.usuarios U, smarthouse.usuarios_preferencias UP, smarthouse.preferencias P, smarthouse.atributos A
WHERE P.id_atributo=A.id AND U.id = UP.id_usuario AND P.id = UP.id_preferencia;

INSERT INTO smarthouse.atributos (id, nombre_dispositivo, nombre_atributo) VALUES
(1, 'televisor', 'canal'),
(2, 'televisor', 'volumen'),
(3, 'televisor', 'encendido'),
(4, 'aire', 'temperatura'),
(5, 'aire', 'velocidad'),
(6, 'aire', 'encendido'),
(7, 'computador', 'sist_op'),
(8, 'computador', 'encendido'),
(9, 'luz', 'intensidad'),
(10, 'luz', 'encendido'),
(11, 'radio', 'banda'),
(12, 'radio', 'emisora'),
(13, 'radio', 'volumen'),
(14, 'radio', 'encendido');


INSERT INTO smarthouse.usuarios (id, nombre) VALUES
(1, 'default'),
(2, 'Martin'),
(3, 'Maria');

INSERT INTO smarthouse.preferencias (id, id_atributo, valor, hora, dia) VALUES
(1, 11, 'FM', '6', 'monday'),
(2, 12, '92.3', '6', 'monday'),
(3, 13, '20', '6', 'monday'),
(4, 12, '89.3', '6', 'monday'),
(5, 1, '58', '15', 'thursday'),
(6, 2, '25', '15', 'thursday'),
(7, 1, '56', '15', 'thursday'),
(8, 2, '20', '15', 'thursday'),
(9, 4, '20', '15', 'thursday'),
(10, 5, '30', '15', 'thursday'),
(11, 7, 'Unix/Linux', '15', 'thursday'),
(12, 9, '100', '15', 'thursday'),
(13, 14, 'no', '15', 'thursday'),
(14, 1, '56', '14', 'tuesday'),
(15, 2, '40', '14', 'tuesday'),
(16, 4, '18', '14', 'tuesday'),
(17, 5, '50', '14', 'tuesday'),
(18, 8, 'no', '14', 'tuesday'),
(19, 9, '50', '14', 'tuesday'),
(20, 14, 'no', '14', 'tuesday'),
(21, 1, '15', '14', 'tuesday'),
(22, 3, 'no', '6', 'monday'),
(23, 4, '16', '6', 'monday'),
(24, 5, '80', '6', 'monday'),
(25, 10, 'no', '6', 'monday'),
(26, 9, '50', '7', 'monday'),
(27, 1, '9', '21', 'monday'),
(28, 2, '70', '21', 'monday'),
(29, 4, '18', '21', 'monday'),
(30, 5, '50', '21', 'monday'),
(31, 8, 'no', '21', 'monday'),
(32, 9, '150', '21', 'monday'),
(33, 14, 'no', '21', 'monday');


INSERT INTO smarthouse.usuarios_preferencias (id_usuario, id_preferencia, popularidad) VALUES
(2, 1, 30),
(2, 2, 15),
(2, 3, 30),
(2, 4, 16),
(2, 5, 40),
(2, 6, 80),
(2, 7, 39),
(2, 8, 60),
(2, 9, 60),
(2, 10, 60),
(2, 11, 60),
(2, 12, 50),
(2, 13, 60),
(2, 14, 75),
(2, 15, 80),
(2, 16, 60),
(2, 17, 60),
(2, 18, 70),
(2, 19, 60),
(2, 20, 60),
(2, 21, 74),
(2, 22, 50),
(2, 23, 50),
(2, 24, 50),
(2, 25, 50),
(2, 26, 50),
(3, 27, 50),
(3, 28, 50),
(3, 29, 50),
(3, 30, 50),
(3, 31, 50),
(3, 32, 50),
(3, 33, 50);
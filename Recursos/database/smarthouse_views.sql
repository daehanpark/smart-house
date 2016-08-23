
CREATE OR REPLACE VIEW smarthouse.v_preferencia AS
SELECT P.id,A.nombre_dispositivo,A.nombre_atributo,P.valor,P.hora,P.dia
FROM smarthouse.preferencias P, smarthouse.atributos A
WHERE P.id_atributo=A.id;

CREATE OR REPLACE VIEW smarthouse.v_preferencia_usuarios AS
SELECT U.id as id_usuario, P.id as id_preferencia, U.nombre as nombre_usuario, A.nombre_dispositivo,A.nombre_atributo,P.valor,P.hora,P.dia, UP.popularidad
FROM smarthouse.usuarios U, smarthouse.usuarios_preferencias UP, smarthouse.preferencias P, smarthouse.atributos A
WHERE P.id_atributo=A.id AND U.id = UP.id_usuario AND P.id = UP.id_preferencia;


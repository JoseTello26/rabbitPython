CREATE DATABASE tienda;
\c tienda;
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    correo VARCHAR(255),
    pass VARCHAR(255)
);
CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    id_usuario INT,
    id_producto INT,
    cantidad INT
);
INSERT INTO usuarios (nombre, correo, pass) VALUES
  ('Jake Peralta', 'jake.peralta@example.com', 'password1'),
  ('Amy Santiago', 'amy.santiago@example.com', 'password2'),
  ('Terry Jeffords', 'terry.jeffords@example.com', 'password3'),
  ('Rosa Diaz', 'rosa.diaz@example.com', 'password4'),
  ('Raymond Holt', 'raymond.holt@example.com', 'password5'),
  ('Gina Linetti', 'gina.linetti@example.com', 'password6'),
  ('Charles Boyle', 'charles.boyle@example.com', 'password7'),
  ('Hitchcock Scully', 'hitchcock.scully@example.com', 'password8'),
  ('Adrian Pimento', 'adrian.pimento@example.com', 'password9'),
  ('Kevin Cozner', 'kevin.cozner@example.com', 'password10');


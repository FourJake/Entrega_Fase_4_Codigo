-- Ejecutar UNA VEZ en una base nueva. No elimina ni reemplaza datos existentes.
CREATE DATABASE IF NOT EXISTS proyecto_w_python
    CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE proyecto_w_python;

create table users (
	id_user INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(50),
    surname VARCHAR(50),
    admin BOOLEAN
);
create table  if not exists  proveedores (
	id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    proveedor_name VARCHAR(50),
    direccion VARCHAR(50)
);
create table product (
	id_product INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(50),
    stock INT,
    price FLOAT,
    id_proveedor INT,
    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id_proveedor)
);
create table movimientos(
	id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
    id_product INT,
    id_user INT,
    FOREIGN KEY (id_product) REFERENCES product(id_product),
    FOREIGN KEY (id_user) REFERENCES users(id_user),
    cambio INT
);

INSERT INTO users (user_name, surname, admin) VALUES
('Alexis', 'Dapas', TRUE),
('Juan', 'Perez', FALSE);

INSERT INTO proveedores (proveedor_name, direccion) VALUES
('Distribuidora Norte', 'Av. Colon 123'),
('Tecnologia Sur', 'Av. Sabattini 456'),
('Electronica Centro', 'Bv. San Juan 789'),
('Importadora Cordoba', 'Av. Velez Sarsfield 321'),
('Proveedora Digital', 'Ruta 20 654');

INSERT INTO product (product_name, stock, price, id_proveedor) VALUES
('Teclado mecanico', 15, 25000, 1),
('Mouse inalambrico', 25, 12000, 1),
('Monitor 24 pulgadas', 10, 150000, 2),
('Notebook', 8, 650000, 2),
('Auriculares', 20, 35000, 3),
('Parlantes', 12, 45000, 3),
('Webcam HD', 18, 30000, 4),
('Disco SSD 1TB', 10, 90000, 4),
('Memoria RAM 16GB', 15, 70000, 5),
('Cable HDMI', 30, 10000, 5);

INSERT INTO movimientos (id_product, id_user, cambio) VALUES
(1, 1, 5),
(2, 2, -2),
(3, 1, 3),
(5, 2, -1);

SELECT 
    product.product_name AS Producto,
    product.stock AS Stock,
    product.price AS Precio,
    proveedores.proveedor_name AS Proveedor
FROM product
INNER JOIN proveedores
ON product.id_proveedor = proveedores.id_proveedor;

SELECT
    movimientos.id_movimiento,
    product.product_name AS Producto,
    users.user_name AS Usuario,
    movimientos.cambio
FROM movimientos
INNER JOIN product
ON movimientos.id_product = product.id_product
INNER JOIN users
ON movimientos.id_user = users.id_user;

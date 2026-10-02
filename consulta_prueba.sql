USE proyecto_w_python;

SELECT p.id_product, p.product_name, p.stock, p.price,
       p.id_proveedor, pr.proveedor_name, pr.direccion
FROM product AS p
LEFT JOIN proveedores AS pr ON p.id_proveedor = pr.id_proveedor
ORDER BY p.id_product;

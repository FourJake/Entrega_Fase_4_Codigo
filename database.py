import os
import mysql.connector
from mysql.connector import Error


def conectar():
    """Abre una conexión usando variables de entorno; no guarda claves en el código."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "proyecto_w_python"),
    )


def obtener_productos():
    """Consulta productos y proveedores y transforma cada fila en un objeto Producto."""
    consulta = """
        SELECT p.id_product, p.product_name, p.stock, p.price,
               p.id_proveedor, pr.proveedor_name
        FROM product AS p
        LEFT JOIN proveedores AS pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_product
    """
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(consulta)
        from producto import Producto
        return [Producto(
            fila["id_product"], fila["product_name"], fila["stock"],
            float(fila["price"]), fila["id_proveedor"], fila["proveedor_name"]
        ) for fila in cursor.fetchall()]
    except Error as error:
        raise RuntimeError(f"No se pudo consultar MySQL: {error}") from error
    finally:
        if cursor is not None:
            cursor.close()
        if conexion is not None and conexion.is_connected():
            conexion.close()

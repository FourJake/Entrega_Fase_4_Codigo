import os
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

from movimiento_stock import MovimientoStock
from producto import Producto
from proveedor import Proveedor
from usuario import Usuario


def conectar():
    """Lee .env junto al código y abre MySQL; el entorno tiene prioridad."""
    load_dotenv(Path(__file__).resolve().with_name(".env"), override=False)
    try:
        puerto = int(os.getenv("DB_PORT", "3306"))
        if not 1 <= puerto <= 65535:
            raise ValueError
    except ValueError as error:
        raise RuntimeError("DB_PORT debe ser un número entero entre 1 y 65535.") from error
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=puerto,
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "proyecto_w_python"),
        connection_timeout=5,
    )


def _consultar(consulta):
    """Recupera filas y libera los recursos incluso si la consulta falla."""
    conexion = None
    cursor = None
    try:
        conexion = conectar()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(consulta)
        return cursor.fetchall()
    except Error as error:
        raise RuntimeError(f"No se pudo consultar MySQL: {error}") from error
    finally:
        try:
            if cursor is not None:
                cursor.close()
        finally:
            if conexion is not None:
                conexion.close()


def _crear_producto(fila):
    proveedor = None
    if fila["proveedor_name"] is not None:
        proveedor = Proveedor(fila["id_proveedor"], fila["proveedor_name"], fila["direccion"])
    return Producto(
        fila["id_product"], fila["product_name"], fila["stock"],
        fila["price"], fila["id_proveedor"], proveedor,
    )


def obtener_productos():
    """Convierte el JOIN de productos y proveedores en objetos relacionados."""
    filas = _consultar("""
        SELECT p.id_product, p.product_name, p.stock, p.price,
               p.id_proveedor, pr.proveedor_name, pr.direccion
        FROM product AS p
        LEFT JOIN proveedores AS pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY p.id_product
    """)
    return [_crear_producto(fila) for fila in filas]


def obtener_proveedores():
    filas = _consultar("""
        SELECT id_proveedor, proveedor_name, direccion
        FROM proveedores ORDER BY id_proveedor
    """)
    return [Proveedor(f["id_proveedor"], f["proveedor_name"], f["direccion"]) for f in filas]


def obtener_usuarios():
    filas = _consultar("""
        SELECT id_user, user_name, surname, admin FROM users ORDER BY id_user
    """)
    return [Usuario(f["id_user"], f["user_name"], f["surname"], f["admin"]) for f in filas]


def obtener_movimientos():
    """Cada movimiento contiene los objetos Producto y Usuario de su registro."""
    filas = _consultar("""
        SELECT m.id_movimiento, m.cambio,
               p.id_product, p.product_name, p.stock, p.price, p.id_proveedor,
               pr.proveedor_name, pr.direccion,
               u.id_user, u.user_name, u.surname, u.admin
        FROM movimientos AS m
        INNER JOIN product AS p ON m.id_product = p.id_product
        INNER JOIN users AS u ON m.id_user = u.id_user
        LEFT JOIN proveedores AS pr ON p.id_proveedor = pr.id_proveedor
        ORDER BY m.id_movimiento
    """)
    return [MovimientoStock(
        f["id_movimiento"], f["id_product"], f["id_user"], f["cambio"],
        _crear_producto(f), Usuario(f["id_user"], f["user_name"], f["surname"], f["admin"]),
    ) for f in filas]

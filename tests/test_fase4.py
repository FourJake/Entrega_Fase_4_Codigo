"""Pruebas de conversión a objetos y manejo de la conexión, sin servidor."""

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import MagicMock, patch

from mysql.connector import Error

import database
import main
from movimiento_stock import MovimientoStock
from producto import Producto
from proveedor import Proveedor
from usuario import Usuario


class PruebasFase4(unittest.TestCase):
    def setUp(self):
        self.fila = {
            "id_product": 1, "product_name": "Yerba", "stock": 5,
            "price": 2500.0, "id_proveedor": 2,
            "proveedor_name": "Distribuidora", "direccion": "Calle 123",
            "id_user": 3, "user_name": "Ana", "surname": "Pérez", "admin": 0,
            "id_movimiento": 4, "cambio": -2,
        }

    def test_productos_contienen_proveedor_y_se_muestran(self):
        with patch("database._consultar", return_value=[self.fila]):
            producto = database.obtener_productos()[0]
        self.assertIsInstance(producto, Producto)
        self.assertIsInstance(producto.proveedor, Proveedor)
        self.assertEqual(producto.proveedor.id, producto.id_proveedor)
        self.assertEqual(producto.mostrar_datos(),
                         "Yerba | Stock: 5 | Precio: $2500.00 | Proveedor: Distribuidora")
        self.assertTrue(producto.tiene_stock_bajo())
        self.assertFalse(producto.tiene_stock_bajo(4))

    def test_producto_sin_proveedor_no_se_pierde(self):
        self.fila.update(id_proveedor=None, proveedor_name=None, direccion=None)
        with patch("database._consultar", return_value=[self.fila]):
            producto = database.obtener_productos()[0]
        self.assertIsNone(producto.proveedor)
        self.assertIn("Sin proveedor", producto.mostrar_datos())

    def test_proveedores_y_usuarios_se_convierten(self):
        with patch("database._consultar", return_value=[self.fila]):
            proveedor = database.obtener_proveedores()[0]
            usuario = database.obtener_usuarios()[0]
        self.assertIsInstance(proveedor, Proveedor)
        self.assertEqual(proveedor.mostrar_datos(), "Distribuidora | Calle 123")
        self.assertIsInstance(usuario, Usuario)
        self.assertFalse(usuario.puede_gestionar())
        self.assertEqual(usuario.mostrar_datos(), "Ana Pérez | Rol: Empleado")
        self.assertTrue(Usuario(1, "Alexis", "Dapas", 1).puede_gestionar())

    def test_movimientos_contienen_producto_y_usuario(self):
        with patch("database._consultar", return_value=[self.fila]):
            movimiento = database.obtener_movimientos()[0]
        self.assertIsInstance(movimiento, MovimientoStock)
        self.assertIsInstance(movimiento.producto, Producto)
        self.assertIsInstance(movimiento.usuario, Usuario)
        self.assertEqual(movimiento.producto.id, movimiento.id_producto)
        self.assertEqual(movimiento.usuario.id, movimiento.id_usuario)
        self.assertEqual(movimiento.mostrar_datos(),
                         "Salida de 2 unidades de Yerba; realizado por Ana Pérez")
        self.assertEqual(MovimientoStock(1, 1, 1, 2).tipo(), "Entrada")
        self.assertEqual(MovimientoStock(1, 1, 1, 0).tipo(), "Sin cambio")

    def test_consulta_libera_recursos_tras_exito_o_error(self):
        for falla in (False, True):
            with self.subTest(falla=falla):
                conexion = MagicMock()
                cursor = conexion.cursor.return_value
                cursor.fetchall.return_value = [self.fila]
                if falla:
                    cursor.execute.side_effect = Error("Tabla inexistente")
                with patch("database.conectar", return_value=conexion):
                    if falla:
                        with self.assertRaisesRegex(RuntimeError, "Tabla inexistente"):
                            database._consultar("SELECT * FROM product")
                    else:
                        self.assertEqual(database._consultar("SELECT * FROM product"), [self.fila])
                cursor.close.assert_called_once()
                conexion.close.assert_called_once()

    def test_fallo_de_conexion_se_informa(self):
        with patch("database.conectar", side_effect=Error("Servidor no disponible")):
            with self.assertRaisesRegex(RuntimeError, "Servidor no disponible"):
                database.obtener_productos()

    def test_puerto_invalido_se_rechaza_antes_de_conectar(self):
        for puerto in ("texto", "0", "65536"):
            with self.subTest(puerto=puerto), patch("database.load_dotenv"), \
                    patch.dict(os.environ, {"DB_PORT": puerto}), \
                    patch("database.mysql.connector.connect") as conectar:
                with self.assertRaisesRegex(RuntimeError, "DB_PORT"):
                    database.conectar()
                conectar.assert_not_called()

    def test_main_muestra_listados_vacios_y_error_sin_traceback(self):
        salida = io.StringIO()
        with patch("database._consultar", return_value=[]), redirect_stdout(salida):
            self.assertEqual(main.main(), 0)
        self.assertEqual(salida.getvalue().count("No hay registros."), 4)
        salida = io.StringIO()
        with patch("database.conectar", side_effect=Error("Servidor no disponible")), \
                redirect_stdout(salida):
            self.assertEqual(main.main(), 1)
        self.assertIn("Servidor no disponible", salida.getvalue())
        self.assertNotIn("Traceback", salida.getvalue())


if __name__ == "__main__":
    unittest.main()

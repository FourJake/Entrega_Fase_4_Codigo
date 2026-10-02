"""Demostración de la fase 4: MySQL -> objetos -> métodos -> consola."""

import sys


def main():
    try:
        from database import (
            obtener_movimientos, obtener_productos,
            obtener_proveedores, obtener_usuarios,
        )
    except ModuleNotFoundError as error:
        print(f"Falta una dependencia: {error.name}.")
        print("Instalá las dependencias con: python -m pip install -r requirements.txt")
        return 1

    try:
        secciones = [
            ("PRODUCTOS", obtener_productos()),
            ("PROVEEDORES", obtener_proveedores()),
            ("USUARIOS", obtener_usuarios()),
            ("MOVIMIENTOS DE STOCK", obtener_movimientos()),
        ]
        print("SISTEMA DE STOCK - MINIMERCADO EL BARRIO - FASE 4")
        print("Conexión y consultas MySQL realizadas correctamente.")
        for titulo, objetos in secciones:
            print(f"\n{titulo}")
            if not objetos:
                print("No hay registros.")
            for objeto in objetos:
                print(objeto.mostrar_datos())
        return 0
    except RuntimeError as error:
        print(error)
        print("Revisá que MySQL esté activo, que hayas importado 3.sql y la configuración de .env.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

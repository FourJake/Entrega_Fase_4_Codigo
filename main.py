from database import obtener_productos


def main():
    try:
        productos = obtener_productos()
        if not productos:
            print("La consulta no devolvió productos.")
        for producto in productos:
            print(producto.mostrar_datos())
    except RuntimeError as error:
        print(error)
        print("Revisá que MySQL esté activo y que DB_HOST, DB_USER, DB_PASSWORD y DB_NAME sean correctos.")


if __name__ == "__main__":
    main()

class Proveedor:
    """Almacena los datos de un proveedor; puede suministrar varios productos."""

    def __init__(self, id_proveedor, proveedor_name, direccion):
        self.id = id_proveedor
        self.nombre = proveedor_name
        self.direccion = direccion

    def mostrar_datos(self):
        return f"{self.nombre} | {self.direccion}"

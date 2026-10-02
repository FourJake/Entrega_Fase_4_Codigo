class Producto:
    """Representa un artículo y el proveedor que lo suministra."""

    def __init__(self, id_product, product_name, stock, price, id_proveedor, proveedor_name=None):
        self.id = id_product
        self.nombre = product_name
        self.stock = stock
        self.precio = price
        self.id_proveedor = id_proveedor
        self.proveedor = proveedor_name

    def mostrar_datos(self):
        if hasattr(self.proveedor, "nombre"):
            proveedor = self.proveedor.nombre
        else:
            proveedor = self.proveedor or (f"ID {self.id_proveedor}" if self.id_proveedor is not None else "Sin proveedor")
        return f"{self.nombre} | Stock: {self.stock} | Precio: ${self.precio:.2f} | Proveedor: {proveedor}"

    def tiene_stock_bajo(self, minimo=5):
        return self.stock <= minimo

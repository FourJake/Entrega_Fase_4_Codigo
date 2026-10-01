class MovimientoStock:
    def __init__(self, id_movimiento, id_product, id_user, cambio, producto=None, usuario=None):
        self.id = id_movimiento
        self.id_producto = id_product
        self.id_usuario = id_user
        self.cambio = cambio
        self.producto = producto
        self.usuario = usuario

    def tipo(self):
        if self.cambio > 0:
            return "Entrada"
        if self.cambio < 0:
            return "Salida"
        return "Sin cambio"

    def mostrar_datos(self):
        nombre_producto = self.producto or f"Producto {self.id_producto}"
        nombre_usuario = self.usuario or f"Usuario {self.id_usuario}"
        return f"{self.tipo()} de {abs(self.cambio)} unidades de {nombre_producto}; realizado por {nombre_usuario}"

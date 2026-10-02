class Usuario:
    """Representa una persona y su rol según el campo admin de MySQL."""

    def __init__(self, id_user, user_name, surname, admin):
        self.id = id_user
        self.nombre = user_name
        self.apellido = surname
        self.es_admin = bool(admin)

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def puede_gestionar(self):
        return self.es_admin

    def mostrar_datos(self):
        rol = "Administrador" if self.puede_gestionar() else "Empleado"
        return f"{self.nombre_completo()} | Rol: {rol}"

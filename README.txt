FASE 4 - SISTEMA DE GESTIÓN DE STOCK DEL MINIMERCADO EL BARRIO

Alcance
Diseño e implementación inicial de Producto, Proveedor, Usuario y MovimientoStock.
La aplicación consulta MySQL, crea objetos relacionados y muestra sus datos
mediante los métodos de cada clase. El CRUD corresponde a la fase 5; el login,
la herencia y el registro de nuevos movimientos corresponden a la fase 6.

Requisitos
- Python 3.10 o posterior.
- Servidor MySQL instalado y en ejecución.
- Dependencias: python -m pip install -r requirements.txt

Preparación de la base
Si todavía no existe, ejecutar 3.sql desde MySQL Workbench (abrir el archivo
y ejecutar el script completo), o desde el cliente mysql:
  source C:/Users/Alexis/Desktop/Proyectos web/Entrega_Fase_4_Codigo/3.sql
El archivo crea proyecto_w_python, sus cuatro tablas y los datos iniciales
de la etapa anterior: 2 usuarios, 5 proveedores, 10 productos y 4 movimientos.
Usarlo una sola vez en una base nueva. Si las tablas ya existen y contienen
los datos de la etapa 3, no volver a importar el script.
Los movimientos iniciales son registros de ejemplo, no operaciones que esta
demostración aplique de nuevo sobre el stock actual.

Configuración en PowerShell
  Copy-Item .env.ejemplo .env
Editar .env y completar DB_PASSWORD con la contraseña del servidor MySQL.
DB_HOST, DB_PORT, DB_USER y DB_NAME tienen valores de ejemplo locales.
Las variables del entorno, si existen, tienen prioridad sobre .env.
.env se lee desde la carpeta del código y está excluido de Git.
No entregar contraseñas junto con el proyecto.

Ejecución
  python main.py
La consola muestra productos con su proveedor, proveedores, usuarios con su
rol y movimientos con el producto y el usuario correspondiente.
Un listado vacío muestra "No hay registros.". Una conexión fallida informa
el error y termina con código 1; una ejecución correcta termina con código 0.

Archivos de la entrega
- DISEÑO_FASE_4.md: justificación de clases, atributos, métodos y diagrama.
- producto.py, proveedor.py, usuario.py y movimiento_stock.py: clases iniciales.
- database.py: configuración, conexión, SELECT/JOIN y conversión a objetos.
- main.py: demostración por consola.
- 3.sql: creación de la base de datos y datos iniciales.
- consulta_prueba.sql: SELECT con JOIN para comparar con los objetos Producto.
- requirements.txt y .env.ejemplo: dependencias y configuración de ejemplo.

Pruebas automatizadas
  python -m unittest discover -s tests -v
Estas pruebas no necesitan un servidor: simulan la conexión para comprobar
la conversión a objetos, las relaciones y el cierre de recursos ante errores.
La verificación real requiere ejecutar main.py contra un servidor MySQL.

Verificación realizada para esta entrega
Se importó 3.sql en un servidor MySQL 8.4 temporal y aislado. main.py terminó
con código 0 y mostró los 10 productos, 5 proveedores, 2 usuarios y 4 movimientos,
con sus relaciones convertidas en objetos. También pasaron las 8 pruebas
automatizadas. El servidor temporal se cerró al finalizar la comprobación;
para usar la aplicación se debe configurar el servidor propio como se indica arriba.

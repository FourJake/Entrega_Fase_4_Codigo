FASE 4 - SISTEMA DE GESTION DE STOCK

Requisitos: Python 3 y MySQL Connector.
Instalacion: python -m pip install mysql-connector-python

Antes de ejecutar: verificar que exista proyecto_w_python y que sus tablas
se llamen users, proveedores, product y movimientos, según las etapas anteriores.
Configurar DB_HOST, DB_PORT, DB_USER, DB_PASSWORD y DB_NAME en el entorno.
En Windows CMD, por ejemplo:
  set DB_HOST=localhost
  set DB_USER=root
  set DB_PASSWORD=tu_clave
  set DB_NAME=proyecto_w_python

Ejecutar desde esta carpeta: python main.py
El programa consulta los productos con LEFT JOIN a proveedores, instancia objetos
Producto y muestra sus datos. La clave permanece fuera de los archivos.

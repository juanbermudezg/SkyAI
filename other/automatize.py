import mysql.connector

# Configuración de la conexión a la base de datos
config = {
    'user': 'root',
    'password': 'esave2021',
    'host': 'localhost',
    'database': 'skydb'
}

# Conectar a la base de datos
connection = mysql.connector.connect(**config)
cursor = connection.cursor()

# Datos para insertar
airliners = [
    {'name': 'Avianca', 'path2image': '/static/src/Airlines/Avianca.jpg', 'id2ai': 1},
    {'name': 'LATAM Airlines', 'path2image': '/static/src/Airlines/LATAM.png', 'id2ai': 2},
    {'name': 'JetSMART', 'path2image': '/static/src/Airlines/JetSMART.png', 'id2ai': 3},
    {'name': 'Clic Air', 'path2image': '/static/src/Airlines/Clic.jpg', 'id2ai': 3},
    {'name': 'Satena', 'path2image': '/static/src/Airlines/SATENA.png', 'id2ai': 3},
]

# Insertar datos en la tabla
for airliner in airliners:
    cursor.execute(
        """
        INSERT INTO sky_airliner (name, path2image, id2ai) 
        VALUES (%s, %s, %s)
        """,
        (airliner['name'], airliner['path2image'], airliner['id2ai'])
    )

# Confirmar cambios
connection.commit()

# Cerrar cursor y conexión
cursor.close()
connection.close()

print("Datos insertados correctamente.")

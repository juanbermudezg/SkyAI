import mysql.connector


config = {
    'user': 'root',
    'password': 'esave2021',
    'host': 'localhost',
    'database': 'skydb'
}


connection = mysql.connector.connect(**config)
cursor = connection.cursor()


for _ in range(1):  
   
    nameAirport = input("Ingrese el nombre del aeropuerto: ")
    nameCity = input("Ingrese el nombre de la ciudad: ")
    nameCountry = int(input("Ingrese el ID del país: ")) 
    IATA_Code = input("Ingrese el código IATA: ")


    cursor.execute(
        """
        INSERT INTO sky_locationairport (nameAirport, nameCity, nameCountry_id, IATA_Code) 
        VALUES (%s, %s, %s, %s)
        """,
        (nameAirport, nameCity, nameCountry, IATA_Code)
    )


connection.commit()


cursor.close()
connection.close()

print("Datos insertados correctamente.")

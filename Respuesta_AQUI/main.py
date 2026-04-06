import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import io


# Ejercicio 1

# Asegúrate de que tienes instalados los paquetes pandas y requests de Python para poder trabajar en el proyecto.
# En el caso de que no tengas las librerías instaladas, ejecuta en la consola:

# pip install pandas requests lxml

# Ejercicio 2

url = "https://www.growbarato.net/"

response = requests.get(url, headers=headers)
print(f"El código ha obtenido una respuesta con el estado: {response.status_code}")

# Ejercicio 3 - Transformar el HTML con BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")

# Los productos están en etiquetas <article class="product-miniature">
productos = soup.find_all("article", {"class": "product-miniature"})
print(f"Productos encontrados: {len(productos)}")

datos = []
for producto in productos:
    nombre = producto.find("p", {"class": "product-title"})

# # <p class="product-title">
#     Flores de CBD Small Buds Gorilla Grillz
# </p>

    precio = producto.find("span", {"class": "price"})
    enlace = producto.find("a", {"class": "product-thumbnail"})

    datos.append({
        "nombre": nombre.text.strip() if nombre else None,
        "precio": precio.text.strip() if precio else None,
        "url": enlace["href"] if enlace else None
    })

# Ejercicio 4 - Procesar el DataFrame

df = pd.DataFrame(datos)


df = df.dropna(how="all")

df = df.dropna(subset=["nombre", "precio"])

df = df.reset_index(drop=True)


print(df)


# Ejercicio 5 - Guardar en SQLite

conn = sqlite3.connect("productos.db")
cursor = conn.cursor()

# Creamos tabla!
cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        precio TEXT,
        url TEXT
    )
""")

for _, fila in df.iterrows():
    cursor.execute("""
        INSERT INTO productos (nombre, precio, url)
        VALUES (?, ?, ?)
    """, (fila["nombre"], fila["precio"], fila["url"]))

conn.commit()
conn.close()
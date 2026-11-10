import sqlite3

conexion = sqlite3.connect('hospital.db')

conexion.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    turno INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    edad INTEGER,
    motivo TEXT,
    tipo TEXT,
    tiempo INTEGER,
    estado TEXT,
    hora TEXT
)
""")

conexion.commit()
conexion.close()
print("Base de datos creada")
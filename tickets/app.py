import web
import sqlite3
import controllers.index
import controllers.atender
import controllers.siguiente
import controllers.estado

urls = (
    '/', 'controllers.index.Index',
    '/atender', 'controllers.atender.Atender',
    '/siguiente', 'controllers.siguiente.Siguiente',
    '/estado', 'controllers.estado.Estado',
)

app = web.application(urls, globals())

def crear_bd():
    conn = sqlite3.connect("tickets.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_cliente TEXT,
            descripcion TEXT,
            prioridad TEXT,
            tiempo_estimado INTEGER
        )
    """)
    conn.close()

if __name__ == "__main__":
    crear_bd()
    app.run()
    
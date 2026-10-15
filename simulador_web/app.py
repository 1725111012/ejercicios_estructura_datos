import web
import sqlite3
import controllers.index
import controllers.regresar
import controllers.actual
import controllers.historial
import controllers.vaciar
import controllers.salir

urls = (
    '/', 'controllers.index.Index',
    '/regresar', 'controllers.regresar.Regresar',
    '/actual', 'controllers.actual.Actual',
    '/historial', 'controllers.historial.Historial',
    '/vaciar', 'controllers.vaciar.Vaciar',
    '/salir', 'controllers.salir.Salir',
)

app = web.application(urls, globals())

def crear_bd():
    conn = sqlite3.connect("historial.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT
        )
    """)
    conn.close()

if __name__ == "__main__":
    crear_bd()
    app.run()
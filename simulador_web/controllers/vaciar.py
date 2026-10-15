import web
import sqlite3

render = web.template.render('views/')

class Vaciar:
    def GET(self):
        conn = sqlite3.connect("historial.db")
        paginas = conn.execute("SELECT * FROM historial").fetchall()
        total = len(paginas)
        conn.close()
        return render.vaciar(total, None)

    def POST(self):
        conn = sqlite3.connect("historial.db")
        conn.execute("DELETE FROM historial")
        conn.commit()
        conn.close()
        return render.vaciar(0, "Historial eliminado.")
    
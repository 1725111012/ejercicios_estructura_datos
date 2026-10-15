import web
import sqlite3

render = web.template.render('views/')

class Historial:
    def GET(self):
        conn = sqlite3.connect("historial.db")
        paginas = conn.execute("SELECT * FROM historial ORDER BY id DESC").fetchall()
        total = len(paginas)
        conn.close()
        return render.historial(paginas, total)
    
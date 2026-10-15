import web
import sqlite3

render = web.template.render('views/')

class Actual:
    def GET(self):
        conn = sqlite3.connect("historial.db")
        pagina = conn.execute("SELECT * FROM historial ORDER BY id DESC LIMIT 1").fetchone()
        conn.close()
        return render.actual(pagina)
    
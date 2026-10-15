import web
import sqlite3

render = web.template.render('views/')

class Regresar:
    def GET(self):
        conn = sqlite3.connect("historial.db")
        paginas = conn.execute("SELECT * FROM historial ORDER BY id DESC LIMIT 2").fetchall()

        if len(paginas) >= 2:
            conn.execute("DELETE FROM historial WHERE id=?", (paginas[0][0],))
            conn.commit()
            conn.close()
            return render.regresar(paginas[0], paginas[1])

        conn.close()
        return render.regresar(None, None)
    
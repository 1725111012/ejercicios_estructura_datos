import web
import sqlite3

render = web.template.render('views/')

class Index:
    def GET(self):
        return render.index(None)

    def POST(self):
        datos = web.input(url="")

        if datos.url == "":
            return render.index("Escribe la dirección de una página.")

        conn = sqlite3.connect("historial.db")
        conn.execute("INSERT INTO historial (url) VALUES (?)", (datos.url,))
        conn.commit()
        conn.close()
        return render.index(f"Ahora estás en {datos.url}")
    
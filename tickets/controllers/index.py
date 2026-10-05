import web
import sqlite3

render = web.template.render('views/')

class Index:
    def GET(self):
        return render.index(None)

    def POST(self):
        datos = web.input(nombre_cliente="", descripcion="", prioridad="normal", tiempo_estimado="")
        conn = sqlite3.connect("tickets.db")
        conn.execute(
            "INSERT INTO tickets (nombre_cliente, descripcion, prioridad, tiempo_estimado) VALUES (?, ?, ?, ?)",
            (datos.nombre_cliente, datos.descripcion, datos.prioridad, datos.tiempo_estimado)
        )
        conn.commit()
        conn.close()
        return render.index(f"Ticket de {datos.nombre_cliente} registrado en la fila {datos.prioridad}.")
    
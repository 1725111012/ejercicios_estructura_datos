import web
import sqlite3

render = web.template.render('views/')

class Siguiente:
    def GET(self):
        conn = sqlite3.connect("tickets.db")

        ticket = conn.execute(
            "SELECT * FROM tickets WHERE prioridad='prioritaria' ORDER BY id LIMIT 1"
        ).fetchone()

        if not ticket:
            ticket = conn.execute(
                "SELECT * FROM tickets WHERE prioridad='normal' ORDER BY id LIMIT 1"
            ).fetchone()

        conn.close()
        return render.siguiente(ticket)
    
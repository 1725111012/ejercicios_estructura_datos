import web
import sqlite3

render = web.template.render('views/')

class Atender:
    def GET(self):
        conn = sqlite3.connect("tickets.db")

        ticket = conn.execute(
            "SELECT * FROM tickets WHERE prioridad='prioritaria' ORDER BY id LIMIT 1"
        ).fetchone()

        if not ticket:
            ticket = conn.execute(
                "SELECT * FROM tickets WHERE prioridad='normal' ORDER BY id LIMIT 1"
            ).fetchone()

        if ticket:
            conn.execute("DELETE FROM tickets WHERE id=?", (ticket[0],))
            conn.commit()

        conn.close()
        return render.atender(ticket)
    
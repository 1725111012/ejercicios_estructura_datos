import web
import sqlite3

render = web.template.render('views/')

class Estado:
    def GET(self):
        conn = sqlite3.connect("tickets.db")

        prioritarios = conn.execute(
            "SELECT * FROM tickets WHERE prioridad='prioritaria' ORDER BY id"
        ).fetchall()

        normales = conn.execute(
            "SELECT * FROM tickets WHERE prioridad='normal' ORDER BY id"
        ).fetchall()

        total_prioritarios = len(prioritarios)
        total_normales = len(normales)
        total_tickets = total_prioritarios + total_normales

        tiempo_total = 0
        for ticket in prioritarios + normales:
            # Validamos si ticket[4] no es None/vacío y si contiene solo dígitos
            val = ticket[4]
            if val is not None and str(val).isdigit():
                tiempo_total += int(val)

        conn.close()
        return render.estado(prioritarios, normales, total_prioritarios, total_normales, total_tickets, tiempo_total)
    
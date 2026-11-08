import web
import modelo

urls = (
    '/', 'Registrar',
    '/filas', 'Filas',
    '/atender', 'Atender',
    '/estadisticas', 'Estadisticas'
)

render = web.template.render('templates/', base='layout')

class Registrar:
    def GET(self):
        return render.registrar()

    def POST(self):
        d = web.input()
        modelo.registrar(d.nombre, int(d.edad), d.motivo, d.tipo, int(d.tiempo))
        raise web.seeother('/filas')


class Filas:
    def GET(self):
        prioritaria = modelo.ver_fila('Prioritaria')
        general = modelo.ver_fila('General')
        return render.filas(prioritaria, general)


class Atender:
    def POST(self):
        modelo.atender_siguiente()
        raise web.seeother('/filas')


class Estadisticas:
    def GET(self):
        total, atendidos, promedio, espera = modelo.estadisticas()
        en_prioritaria = len(modelo.ver_fila('Prioritaria'))
        en_general = len(modelo.ver_fila('General'))
        ultimos = modelo.ver_atendidos()
        return render.estadisticas(total, atendidos, promedio, espera,
                                   en_prioritaria, en_general, ultimos)


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()

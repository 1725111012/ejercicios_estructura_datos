import web

render = web.template.render('views/')

class Salir:
    def GET(self):
        return render.salir()
    
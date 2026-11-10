import web
import modelo

urls = (
    '/', 'Registrar',
    '/filas', 'Filas',
    '/atender', 'Atender',
    '/estadisticas', 'Estadisticas'
)

render = web.template.render('templates/', base='layout')

# Si el motivo de consulta contiene alguna de estas palabras,
# el paciente entra a la fila prioritaria
PALABRAS_PRIORITARIAS = [
    "dolor de pecho", "infarto", "falta de aire", "no puede respirar",
    "dificultad para respirar", "hemorragia", "sangrado", "desmayo",
    "inconsciente", "convulsion", "convulsión", "fractura",
    "quemadura", "accidente", "fiebre alta", "envenenamiento"
]

def clasificar(motivo):
    motivo = motivo.lower()
    for palabra in PALABRAS_PRIORITARIAS:
        if palabra in motivo:
            return "Prioritaria"
    return "General"

class Registrar:
    def GET(self):
        return render.registrar()

    def POST(self):
        datos = web.input()
        tipo = clasificar(datos.motivo)
        turno = modelo.registrar(datos.nombre, int(datos.edad), datos.motivo,
                                 tipo, int(datos.tiempo))
        return render.registrado(turno, tipo)

class Filas:
    def GET(self):
        prioritaria = modelo.ver_fila('Prioritaria')
        general = modelo.ver_fila('General')
        return render.filas(prioritaria, general)

class Atender:
    def POST(self):
        turno = modelo.atender_siguiente()
        paciente = None
        if turno is not None:
            paciente = modelo.ver_paciente(turno)
        return render.atendido(paciente)

class Estadisticas:
    def GET(self):
        total, atendidos, promedio, espera, en_prioritaria, en_general = modelo.estadisticas()
        ultimos = modelo.ver_atendidos()
        return render.estadisticas(total, atendidos, promedio, espera,
                                   en_prioritaria, en_general, ultimos)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
    
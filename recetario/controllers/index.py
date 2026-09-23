import web
import sqlite3

render = web.template.render('recetario/views/')

CATEGORIAS = {

    "Agridulce": ["agridulce", " limon", "catsup", "salsa de soya "],
    "Dulce":     ["pastel", "azucar", "chocolate", "postre", "dulce", "galleta", "helado"],
    "Picosa":    ["chile", "picante", "jalapeno", "habanero"],
    "Mariscos":  ["camaron", "pescado", "marisco", "pulpo", "atun"],
    "Pastas":    ["pasta", "espagueti", "macarron", "lasaña"],
    "Cortes":    ["bistec", "filete", "costilla", "carne"],
    "Aderezos":  ["aderezo", "mayonesa", "vinagreta"],
}

def categorizar(texto):
    texto = texto.lower()
    for categoria, palabras in CATEGORIAS.items():
        for palabra in palabras:
            if palabra in texto:
                return categoria
    return "Salado"

class Index:
    def GET(self):
        return render.index(None)

    def POST(self):
        datos = web.input(nombre="", ingredientes="")
        categoria = categorizar(datos.nombre + " " + datos.ingredientes)

        conn = sqlite3.connect("recetario.db")
        conn.execute(
            "INSERT INTO recetas (nombre, ingredientes, categoria) VALUES (?, ?, ?)",
            (datos.nombre, datos.ingredientes, categoria)
        )
        conn.commit()
        conn.close()

        return render.index(f'"{datos.nombre}" se guardó como {categoria}')
    
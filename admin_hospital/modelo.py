import sqlite3


def conectar():
    conn = sqlite3.connect('hospital.db')
    conn.execute('CREATE TABLE IF NOT EXISTS pacientes ('
                 'turno INTEGER PRIMARY KEY AUTOINCREMENT, '
                 'nombre TEXT, edad INTEGER, motivo TEXT, '
                 'tipo TEXT, tiempo INTEGER, estado TEXT, hora TEXT)')
    return conn


def registrar(nombre, edad, motivo, tipo, tiempo):
    conn = conectar()
    conn.execute("INSERT INTO pacientes (nombre, edad, motivo, tipo, tiempo, estado) "
                 "VALUES (?, ?, ?, ?, ?, 'Esperando')",
                 (nombre, edad, motivo, tipo, tiempo))
    conn.commit()
    conn.close()


def ver_fila(tipo):
    conn = conectar()
    filas = conn.execute("SELECT turno, nombre, edad, motivo, tipo, tiempo FROM pacientes "
                         "WHERE estado='Esperando' AND tipo=? ORDER BY turno", (tipo,)).fetchall()
    conn.close()
    return filas


def ver_atendidos():
    conn = conectar()
    filas = conn.execute("SELECT turno, nombre, edad, motivo, tipo, tiempo FROM pacientes "
                         "WHERE estado='Atendido' ORDER BY hora DESC, turno DESC LIMIT 5").fetchall()
    conn.close()
    return filas


def ver_paciente(turno):
    conn = conectar()
    fila = conn.execute("SELECT turno, nombre, edad, motivo, tipo, tiempo FROM pacientes "
                        "WHERE turno=?", (turno,)).fetchone()
    conn.close()
    return fila


def atender_siguiente():
    conn = conectar()
    sql = "SELECT turno FROM pacientes WHERE estado='Esperando' AND tipo=? ORDER BY turno LIMIT 1"
    fila = conn.execute(sql, ('Prioritaria',)).fetchone()
    if fila is None:
        fila = conn.execute(sql, ('General',)).fetchone()
    turno = None
    if fila is not None:
        turno = fila[0]
        conn.execute("UPDATE pacientes SET estado='Atendido', hora=datetime('now','localtime') "
                     "WHERE turno=?", (turno,))
        conn.commit()
    conn.close()
    return turno


def estadisticas():
    conn = conectar()
    total = conn.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]
    atendidos = conn.execute("SELECT COUNT(*) FROM pacientes WHERE estado='Atendido'").fetchone()[0]
    promedio = conn.execute("SELECT AVG(tiempo) FROM pacientes WHERE estado='Atendido'").fetchone()[0] or 0
    espera = conn.execute("SELECT SUM(tiempo) FROM pacientes WHERE estado='Esperando'").fetchone()[0] or 0
    conn.close()
    return total, atendidos, round(promedio, 1), espera

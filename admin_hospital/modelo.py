import sqlite3

def registrar(nombre, edad, motivo, tipo, tiempo):
    conexion = sqlite3.connect('hospital.db')
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO pacientes (nombre, edad, motivo, tipo, tiempo, estado) " "VALUES (?, ?, ?, ?, ?, 'Esperando')",
                   (nombre, edad, motivo, tipo, tiempo))
    conexion.commit()

    # El turno del paciente recién registrado es el número más alto
    cursor.execute("SELECT MAX(turno) FROM pacientes")
    turno = cursor.fetchone()[0]

    conexion.close()
    return turno


def ver_fila(tipo):
    conexion = sqlite3.connect('hospital.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT turno, nombre, edad, motivo, tipo, tiempo FROM pacientes " "WHERE estado='Esperando' AND tipo=? ORDER BY turno", (tipo,))
    filas = cursor.fetchall()
    conexion.close()
    return filas


def ver_paciente(turno):
    conexion = sqlite3.connect('hospital.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT turno, nombre, edad, motivo, tipo, tiempo FROM pacientes " "WHERE turno=?", (turno,))
    paciente = cursor.fetchone()
    conexion.close()
    return paciente


def ver_atendidos():
    conexion = sqlite3.connect('hospital.db')
    cursor = conexion.cursor()
    cursor.execute("SELECT turno, nombre, edad, motivo, tipo, tiempo FROM pacientes " "WHERE estado='Atendido' ORDER BY hora DESC, turno DESC LIMIT 5")
    filas = cursor.fetchall()
    conexion.close()
    return filas


def atender_siguiente():
    conexion = sqlite3.connect('hospital.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT turno FROM pacientes " "WHERE estado='Esperando' AND tipo='Prioritaria' ORDER BY turno LIMIT 1")
    fila = cursor.fetchone()

    if fila is None:
        cursor.execute("SELECT turno FROM pacientes " "WHERE estado='Esperando' AND tipo='General' ORDER BY turno LIMIT 1")
        fila = cursor.fetchone()

    if fila is None:
        conexion.close()
        return None

    turno = fila[0]
    cursor.execute("UPDATE pacientes SET estado='Atendido', hora=datetime('now','localtime') " "WHERE turno=?", (turno,))
    conexion.commit()
    conexion.close()
    return turno


def estadisticas():
    conexion = sqlite3.connect('hospital.db')
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pacientes WHERE estado='Atendido'")
    atendidos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pacientes " "WHERE estado='Esperando' AND tipo='Prioritaria'")
    en_prioritaria = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pacientes " "WHERE estado='Esperando' AND tipo='General'")
    en_general = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(tiempo) FROM pacientes WHERE estado='Atendido'")
    promedio = cursor.fetchone()[0]
    if promedio is None:
        promedio = 0

    cursor.execute("SELECT SUM(tiempo) FROM pacientes WHERE estado='Esperando'")
    espera = cursor.fetchone()[0]
    if espera is None:
        espera = 0

    conexion.close()
    return total, atendidos, round(promedio, 1), espera, en_prioritaria, en_general

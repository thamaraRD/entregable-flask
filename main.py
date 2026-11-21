
from flask import Flask, render_template, request

app = Flask(__name__)


def calcular_resultado(notas, asistencia):
    promedio = sum(notas) / len(notas)

    if promedio >= 40 and asistencia >= 75:
        estado = "APROBADO"
    else:
        estado = "REPROBADO"

    return round(promedio, 2), estado


def obtener_nombre_mayor(nombres):
    return max(nombres, key=lambda nombre: sum(
        letra.isalpha() for letra in nombre
    ))


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    resultado = None
    error = None

    if request.method == "POST":
        try:
            notas = [
                float(request.form["nota1"]),
                float(request.form["nota2"]),
                float(request.form["nota3"])
            ]
            asistencia = float(request.form["asistencia"])

            if not all(10 <= nota <= 70 for nota in notas):
                error = "Las notas deben estar entre 10 y 70."
            elif not 0 <= asistencia <= 100:
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio, estado = calcular_resultado(
                    notas, asistencia
                )
                resultado = {
                    "promedio": promedio,
                    "estado": estado
                }

        except (ValueError, KeyError):
            error = "Ingresa valores numéricos válidos."

    return render_template(
        "ejercicio1.html",
        resultado=resultado,
        error=error
    )


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    resultado = None
    error = None

    if request.method == "POST":
        nombres = [
            request.form.get("nombre1", "").strip(),
            request.form.get("nombre2", "").strip(),
            request.form.get("nombre3", "").strip()
        ]

        if not all(nombres):
            error = "Debes completar los tres nombres."
        elif any(
            not all(letra.isalpha() or letra.isspace()
                    for letra in nombre)
            for nombre in nombres
        ):
            error = "Los nombres solo deben contener letras."
        elif len(set(nombre.casefold() for nombre in nombres)) != 3:
            error = "Los tres nombres deben ser diferentes."
        else:
            nombre_mayor = obtener_nombre_mayor(nombres)
            cantidad = sum(
                letra.isalpha() for letra in nombre_mayor
            )

            resultado = {
                "nombre": nombre_mayor,
                "cantidad": cantidad
            }

    return render_template(
        "ejercicio2.html",
        resultado=resultado,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)

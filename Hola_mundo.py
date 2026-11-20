# Fer Vázquez
# 19 de Nov, 2026

from datetime import datetime
import math


def calcular_tarifa(
    hora_entrada: str,
    hora_salida: str,
    tarifa_primera_hora: float = 25.0,
    tarifa_fraccion: float = 10.0,
    minutos_fraccion: int = 30,
    minutos_gracia: int = 15,
    tope_diario: float = 200.0,
) -> dict:
    formato = "%Y-%m-%d %H:%M:%S"
    entrada = datetime.strptime(hora_entrada, formato)
    salida = datetime.strptime(hora_salida, formato)

    if salida < entrada:
        raise ValueError(
            "La hora de salida no puede ser anterior a la de entrada."
        )

    minutos_totales = math.ceil((salida - entrada).total_seconds() / 60)

    if minutos_totales <= minutos_gracia:
        total = 0.0
        concepto = "Tiempo de gracia"
    elif minutos_totales <= 60:
        total = tarifa_primera_hora
        concepto = "Primera hora"
    else:
        fracciones = math.ceil((minutos_totales - 60) / minutos_fraccion)
        total = tarifa_primera_hora + (fracciones * tarifa_fraccion)
        concepto = f"1ra hora + {fracciones} fracción(es)"

    dias = max(1, math.ceil(minutos_totales / 1440))
    if total > tope_diario * dias:
        total = tope_diario * dias
        concepto += " (Tope diario aplicado)"

    return {
        "minutos": minutos_totales,
        "costo": round(total, 2),
        "concepto": concepto,
    }


if __name__ == "__main__":
    # Simulación visible en la etapa de Build
    resultado = calcular_tarifa("2026-11-20 10:00:00", "2026-11-20 12:15:00")
    print("=== RESUMEN DE TARIFA EN BUILD ===")
    print(f"Tiempo total: {resultado['minutos']} min")
    print(f"Concepto:     {resultado['concepto']}")
    print(f"Costo Final:  ${resultado['costo']:.2f}")
    print("==================================")

# Fer Vázquez
# 19 de Nov, 2026

from datetime import datetime
import math


def calcular_tarifa_estacionamiento(
    hora_entrada: str,
    hora_salida: str,
    tarifa_primera_hora: float = 25.0,
    tarifa_fraccion: float = 10.0,
    minutos_fraccion: int = 30,
    minutos_gracia: int = 15,
    tope_diario: float = 200.0,
) -> dict:
    """Calcula el costo de estacionamiento basado en timestamps ISO o 'YYYY-MM-DD HH:MM:SS'."""
    formato = "%Y-%m-%d %H:%M:%S"
    entrada = datetime.strptime(hora_entrada, formato)
    salida = datetime.strptime(hora_salida, formato)

    if salida < entrada:
        raise ValueError(
            "La hora de salida no puede ser anterior a la hora de entrada."
        )

    diferencia_segundos = (salida - entrada).total_seconds()
    minutos_totales = math.ceil(diferencia_segundos / 60)

    # 1. Validar tiempo de gracia
    if minutos_totales <= minutos_gracia:
        return {
            "minutos_totales": minutos_totales,
            "total_pagar": 0.0,
            "detalle": "Dentro del tiempo de gracia",
        }

    # 2. Cobro base (primera hora)
    if minutos_totales <= 60:
        total = tarifa_primera_hora
        detalle = "Tarifa base (primera hora)"
    else:
        # 3. Cobro por fracciones adicionales después de la primera hora
        minutos_extra = minutos_totales - 60
        fracciones_extra = math.ceil(minutos_extra / minutos_fraccion)
        total = tarifa_primera_hora + (fracciones_extra * tarifa_fraccion)
        detalle = f"1ra hora + {fracciones_extra} fracción(es) de {minutos_fraccion} min"

    # 4. Aplicar tope máximo si excede el límite diario (calculado por bloques de 24h)
    dias = max(1, math.ceil(minutos_totales / 1440))
    tope_aplicable = tope_diario * dias

    if total > tope_aplicable:
        total = tope_aplicable
        detalle += f" (Tope máximo de {dias} día(s) aplicado)"

    return {
        "minutos_totales": minutos_totales,
        "total_pagar": round(total, 2),
        "detalle": detalle,
    }


# --- Bloque de ejecución y validación (ideal para CI/CD o Workflows) ---
if __name__ == "__main__":
    # Casos de prueba (assertions) para validar la lógica automáticamente
    caso_gracia = calcular_tarifa_estacionamiento(
        "2026-11-20 10:00:00", "2026-11-20 10:15:00"
    )
    assert caso_gracia["total_pagar"] == 0.0, f"Error en gracia: {caso_gracia}"

    caso_base = calcular_tarifa_estacionamiento(
        "2026-11-20 10:00:00", "2026-11-20 10:45:00"
    )
    assert caso_base["total_pagar"] == 25.0, f"Error en base: {caso_base}"

    caso_fraccion = calcular_tarifa_estacionamiento(
        "2026-11-20 10:00:00", "2026-11-20 11:35:00"
    )
    # 1h (25) + 2 fracciones de 30m (20) = 45.0
    assert (
        caso_fraccion["total_pagar"] == 45.0
    ), f"Error en fracción: {caso_fraccion}"

    caso_tope = calcular_tarifa_estacionamiento(
        "2026-11-20 08:00:00", "2026-11-20 20:00:00"
    )
    assert caso_tope["total_pagar"] == 200.0, f"Error en tope: {caso_tope}"

    print("Todas las validaciones del workflow pasaron correctamente.")

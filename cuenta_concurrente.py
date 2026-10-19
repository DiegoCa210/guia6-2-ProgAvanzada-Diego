
"""Ilustra una condicion de carrera y el uso correcto de Lock."""

import threading
import time

SALDO_INICIAL = 1_000

OPERACIONES = (
    ("Cajero 1", 100, 5),
    ("Cajero 2", -50, 5),
    ("Cajero 3", -20, 5),
)

class CuentaBancaria:
    """Mantiene un saldo que varios hilos pueden modificar."""

    def __init__(self, saldo_inicial: int) -> None:
        """Inicializa el estado y su bloqueo de exclusion mutua."""
        self.saldo = saldo_inicial
        self._lock = threading.Lock()

    def aplicar(self, monto: int, segura: bool) -> None:
        """Aplica un movimiento con o sin proteccion del saldo."""
        if segura:
            with self._lock:
                self._actualizar(monto)
        else:
            self._actualizar(monto)

    def _actualizar(self, monto: int) -> None:
        """Simula una operacion de lectura-modificacion-escritura."""
        saldo_anterior = self.saldo
        time.sleep(0.002)  # Pausa didactica, no recomendada en produccion.
        self.saldo = saldo_anterior + monto

def ejecutar_cajero(
    cuenta: CuentaBancaria,
    monto: int,
    veces: int,
    segura: bool
) -> None:
    """Ejecuta varios movimientos sobre una misma cuenta."""
    for _ in range(veces):
        cuenta.aplicar(monto, segura)

def saldo_esperado() -> int:
    """Calcula el resultado correcto de todas las operaciones."""
    return SALDO_INICIAL + sum(
        monto * veces for _, monto, veces in OPERACIONES
    )

def ejecutar_simulacion(segura: bool) -> int:
    """Ejecuta los cajeros en paralelo y devuelve el saldo final."""
    cuenta = CuentaBancaria(SALDO_INICIAL)

    hilos = [
        threading.Thread(
            target=ejecutar_cajero,
            args=(cuenta, monto, veces, segura),
            name=nombre,
        )
        for nombre, monto, veces in OPERACIONES
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return cuenta.saldo

def main() -> None:
    """Contrasta el saldo sin bloqueo y con bloqueo."""
    print(f"Saldo esperado: {saldo_esperado()}")
    print(f"Sin Lock: {ejecutar_simulacion(segura=False)}")
    print(f"Con Lock: {ejecutar_simulacion(segura=True)}")

if __name__ == "__main__":
    main()

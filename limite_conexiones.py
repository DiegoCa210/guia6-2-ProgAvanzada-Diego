"""Limita el acceso concurrente a un servicio con Semaphore."""

import threading
import time

CAPACIDAD = 3
SOLICITUDES = 8


class Servicio:
    """Simula un servicio con cupos de atencion limitados."""

    def __init__(self, capacidad: int) -> None:
        """Crea el semaforo y protege el contador de accesos."""
        if capacidad < 1:
            raise ValueError("La capacidad debe ser positiva.")

        self._semaforo = threading.Semaphore(capacidad)
        self._lock = threading.Lock()
        self._activas = 0
        self.maximo_observado = 0

    def atender(self, numero: int) -> None:
        """Procesa una solicitud sin superar la capacidad asignada."""
        with self._semaforo:
            with self._lock:
                self._activas += 1
                self.maximo_observado = max(
                    self.maximo_observado, self._activas
                )

                print(f"Solicitud {numero}: activas={self._activas}")

            try:
                time.sleep(0.12)  # Simula una consulta o servicio de red.
            finally:
                with self._lock:
                    self._activas -= 1


def ejecutar_simulacion(capacidad: int = CAPACIDAD) -> int:
    """Lanza solicitudes concurrentes y devuelve el pico medido."""
    servicio = Servicio(capacidad)

    hilos = [
        threading.Thread(
            target=servicio.atender,
            args=(numero,)
        )
        for numero in range(1, SOLICITUDES + 1)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return servicio.maximo_observado


def main() -> None:
    """Muestra el maximo de solicitudes atendidas a la vez."""
    maximo = ejecutar_simulacion()
    print(f"Capacidad: {CAPACIDAD}; maximo observado: {maximo}")


if __name__ == "__main__":
    main()
"""Compara Lock y RLock sin provocar un bloqueo permanente."""

import threading


class Registro:
    """Registra eventos desde metodos con llamadas anidadas."""

    def __init__(self) -> None:
        """Inicializa el historial y un bloqueo reentrante."""
        self._eventos: list[str] = []
        self._lock = threading.RLock()

    def registrar(self, evento: str) -> None:
        """Agrega una entrada bajo el bloqueo compartido."""
        with self._lock:
            self._eventos.append(evento)

    def procesar(self) -> tuple[str, ...]:
        """Llama a otro metodo que adquiere el mismo bloqueo."""
        with self._lock:
            self.registrar("Inicio")
            self.registrar("Fin")
            return tuple(self._eventos)


def comprobar_reentrada() -> tuple[bool, bool]:
    """Prueba una segunda adquisicion sin esperar indefinidamente."""
    resultados = []

    for bloqueo in (threading.Lock(), threading.RLock()):
        with bloqueo:
            adquirido = bloqueo.acquire(blocking=False)

            if adquirido:
                bloqueo.release()

            resultados.append(adquirido)

    return resultados[0], resultados[1]


def main() -> None:
    """Muestra el comportamiento de ambos tipos de bloqueo."""
    lock, rlock = comprobar_reentrada()

    print(f"Lock admite reentrada: {lock}")
    print(f"RLock admite reentrada: {rlock}")
    print(f"Historial: {Registro().procesar()}")


if __name__ == "__main__":
    main()
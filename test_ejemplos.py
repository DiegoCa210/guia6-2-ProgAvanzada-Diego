"""Pruebas basicas sin dependencias externas para la guia 6-2."""

import unittest

from cuenta_concurrente import ejecutar_simulacion as ejecutar_banco
from cuenta_concurrente import saldo_esperado
from limite_conexiones import ejecutar_simulacion as ejecutar_servicio
from reentrada import Registro, comprobar_reentrada


class PruebasSincronizacion(unittest.TestCase):
    """Comprueba las propiedades esenciales de los ejemplos seguros."""

    def test_cuenta_protegida(self) -> None:
        """El saldo correcto se obtiene despues de todos los hilos."""
        self.assertEqual(ejecutar_banco(segura=True), saldo_esperado())

    def test_reentrada(self) -> None:
        """Lock no es reentrante y RLock si lo es."""
        self.assertEqual(comprobar_reentrada(), (False, True))
        self.assertEqual(Registro().procesar(), ("Inicio", "Fin"))

    def test_capacidad_semaforo(self) -> None:
        """Nunca se excede el cupo del recurso compartido."""
        maximo = ejecutar_servicio(capacidad=3)
        self.assertLessEqual(maximo, 3)
        self.assertGreaterEqual(maximo, 1)


if __name__ == "__main__":
    unittest.main()
import unittest
from unittest.mock import patch

from app import (
    actualizar_clasificacion,
    actualizar_exploracion,
    comparar_regresiones,
    df,
    experimentos,
    obtener_prefijo_rutas,
)


class DashboardAcademicoTest(unittest.TestCase):
    def test_muestra_reproducible(self):
        self.assertEqual(len(df), 100)
        self.assertAlmostEqual(df["Horas_Estudio_Semana"].mean(), 11.61, places=1)
        self.assertAlmostEqual(df["Puntaje_Examen"].mean(), 72.31, places=1)
        self.assertAlmostEqual(df["Aprobado"].mean(), 0.58, places=2)

    def test_comparacion_de_regresiones(self):
        resultados = comparar_regresiones(df)
        self.assertEqual(len(resultados), 3)
        self.assertTrue((resultados["MSE"] > 0).all())
        self.assertTrue(resultados["R2"].between(0, 1).all())

    def test_experimentos_logisticos(self):
        self.assertEqual(len(experimentos), 6)
        self.assertEqual(set(experimentos["C"]), {0.1, 1.0, 10.0})
        self.assertEqual(set(experimentos["Solver"]), {"liblinear", "lbfgs"})

    def test_callback_exploratorio(self):
        salida = actualizar_exploracion([2, 19], [45, 100], "Todos")
        self.assertEqual(len(salida), 13)
        self.assertEqual(salida[2], "100")
        self.assertEqual(salida[5], "58.0%")
        self.assertEqual(salida[6], "0.896")

    def test_callback_clasificacion(self):
        salida = actualizar_clasificacion(0.5)
        self.assertEqual(len(salida), 5)
        self.assertTrue(salida[2].endswith("%"))
        self.assertTrue(salida[3].endswith("%"))
        self.assertTrue(salida[4].endswith("%"))

    def test_prefijo_binder(self):
        entorno = {"JUPYTERHUB_SERVICE_PREFIX": "/user/prueba/", "DASH_PORT": "8050"}
        with patch.dict("os.environ", entorno, clear=False):
            self.assertEqual(obtener_prefijo_rutas(), "/user/prueba/proxy/8050/")


if __name__ == "__main__":
    unittest.main(verbosity=2)

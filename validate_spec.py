"""
Suite de validación automatizada para la especificación SRS y planificación Scrum de Agroflow.
Verifica la consistencia de datos, stakeholders, módulos funcionales y sumatoria de sprints.
"""

import json
import os
import unittest


class TestAgroflowSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec_path = os.path.join(os.path.dirname(__file__), "srs-agroflow.json")
        with open(spec_path, "r", encoding="utf-8") as f:
            cls.spec = json.load(f)

    def test_metadatos_basicos(self):
        self.assertEqual(self.spec.get("project"), "Agroflow")
        self.assertIn("David Leonardo Martínez", self.spec.get("author", ""))
        self.assertTrue(len(self.spec.get("domain", "")) > 0)

    def test_stakeholders_completos(self):
        stakeholders = self.spec.get("stakeholders", [])
        self.assertEqual(len(stakeholders), 4, "Deben existir exactamente 4 grupos de stakeholders")
        for stk in stakeholders:
            self.assertIn("name", stk)
            self.assertIn("role", stk)
            self.assertIn("benefit", stk)

    def test_modulos_funcionales(self):
        modulos = self.spec.get("functional_modules", [])
        self.assertGreaterEqual(len(modulos), 4, "Deben existir al menos 4 módulos funcionales clave")
        nombres = [m["module"] for m in modulos]
        self.assertIn("Autenticación y Perfiles", nombres)
        self.assertIn("Agricultor (Oferta)", nombres)
        self.assertIn("Comerciante (Demanda)", nombres)
        self.assertIn("Logística (Transportistas)", nombres)

    def test_requerimientos_no_funcionales(self):
        nfr = self.spec.get("non_functional_requirements", {})
        claves_esperadas = ["security", "performance", "usability", "connectivity", "environmental_impact"]
        for k in claves_esperadas:
            self.assertIn(k, nfr, f"Falta el requerimiento no funcional: {k}")

    def test_epicas_y_sprints_scrum(self):
        epicas = self.spec.get("epics", [])
        self.assertEqual(len(epicas), 5, "Deben registrarse 5 épicas de producto")

        sprints = self.spec.get("sprints", [])
        self.assertEqual(len(sprints), 3, "Deben existir 3 sprints planificados")

        for s in sprints:
            self.assertEqual(s["duration_days"], 10, f"El sprint {s['sprint']} debe durar exactamente 10 días")
            total_dias_historias = sum(item["days"] for item in s["items"])
            self.assertEqual(
                total_dias_historias, 
                10, 
                f"La suma de días de las historias en el Sprint {s['sprint']} debe ser 10"
            )


if __name__ == "__main__":
    unittest.main()

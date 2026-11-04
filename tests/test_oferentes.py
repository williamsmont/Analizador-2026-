import unittest
from unittest import mock

from orions import oferentes as o


class TestOferentes(unittest.TestCase):
    def test_extraer_codigos(self):
        t = "557639-3609-cot26 tiene cotizantes? y 1234-56-COT26, otra vez 557639-3609-COT26"
        self.assertEqual(o.extraer_codigos(t), ["557639-3609-COT26", "1234-56-COT26"])
        self.assertEqual(o.extraer_codigos("hola"), [])

    def test_sin_oferentes(self):
        r = o.interpretar("X-1-COT26", {"payload": {"nombre": "Insumos", "proveedores_cotizando": []}})
        self.assertFalse(r.tiene_oferentes)
        self.assertIn("NO tiene oferentes", o.formatear_mensaje(r))

    def test_con_oferentes(self):
        data = {
            "nombre": "Insumos de oficina",
            "institucion": {"organismo_comprador": "Muni"},
            "proveedores_cotizando": [{"razon_social": "ACME SpA"}, {"nombre": "Beta Ltda"}],
        }
        r = o.interpretar("X-1-COT26", data)
        self.assertTrue(r.tiene_oferentes)
        self.assertEqual(r.proveedores, ["ACME SpA", "Beta Ltda"])
        msg = o.formatear_mensaje(r)
        self.assertIn("2 proveedores", msg)
        self.assertIn("ACME SpA", msg)

    def test_campo_ausente(self):
        r = o.interpretar("X-1-COT26", {"nombre": "Algo"})
        self.assertIsNone(r.tiene_oferentes)
        self.assertIn("no informó", o.formatear_mensaje(r))

    def test_responder_usa_api(self):
        fake = {"nombre": "Insumos", "proveedores_cotizando": ["Proveedor A"]}
        with mock.patch.object(o, "_get_json", return_value=fake) as g:
            msg = o.responder("¿557639-3609-COT26 tiene cotizantes?", ticket="T")
        g.assert_called_once_with(f"{o.BASE_URL}/557639-3609-COT26", "T")
        self.assertIn("1 proveedor cotizando", msg)
        self.assertIsNone(o.responder("hola", ticket="T"))

    def test_sin_ticket(self):
        with mock.patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(o.OrionsError):
                o.consultar_oferentes("X-1-COT26")


if __name__ == "__main__":
    unittest.main()

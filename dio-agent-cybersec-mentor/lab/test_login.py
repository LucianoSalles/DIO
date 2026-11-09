"""Prova, no laboratório, que o SQL Injection existe no app.py e foi mitigado no app_fixed.py.

Rode dentro da pasta lab/:  python -m unittest -v test_login.py
"""

import unittest

import app
import app_fixed

# Entradas clássicas de SQL Injection em formulário de login.
ENTRADAS_MALICIOSAS = [
    ("admin' --", "qualquer"),
    ("' OR '1'='1' --", "qualquer"),
    ("admin", "' OR '1'='1"),
]


class LoginVulneravel(unittest.TestCase):
    def setUp(self):
        self.conn = app.criar_banco()

    def test_login_legitimo(self):
        self.assertIsNotNone(app.login(self.conn, "admin", "S3nha-de-lab!"))

    def test_injecao_entra_sem_senha(self):
        for usuario, senha in ENTRADAS_MALICIOSAS:
            with self.subTest(usuario=usuario, senha=senha):
                self.assertIsNotNone(
                    app.login(self.conn, usuario, senha),
                    "esperado: a injeção burla o login vulnerável",
                )


class LoginCorrigido(unittest.TestCase):
    def setUp(self):
        self.conn = app_fixed.criar_banco()

    def test_login_legitimo(self):
        self.assertEqual(app_fixed.login(self.conn, "admin", "S3nha-de-lab!")[1], "admin")

    def test_senha_errada(self):
        self.assertIsNone(app_fixed.login(self.conn, "admin", "errada"))

    def test_injecao_bloqueada(self):
        for usuario, senha in ENTRADAS_MALICIOSAS:
            with self.subTest(usuario=usuario, senha=senha):
                self.assertIsNone(app_fixed.login(self.conn, usuario, senha))

    def test_senha_nao_fica_em_texto_puro(self):
        _, senha_hash = self.conn.execute(
            "SELECT salt, senha_hash FROM usuarios WHERE usuario = 'admin'"
        ).fetchone()
        self.assertNotIn(b"S3nha-de-lab!", senha_hash)


if __name__ == "__main__":
    unittest.main(verbosity=2)

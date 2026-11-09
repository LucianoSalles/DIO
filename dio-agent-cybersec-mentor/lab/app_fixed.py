"""Versão corrigida do login de laboratório.

Mudanças em relação ao app.py:
1. Consulta parametrizada: o que a pessoa digita vai como dado, nunca como SQL.
2. Senha guardada com hash e salt (PBKDF2), em vez de texto puro.
3. Comparação em tempo constante.
"""

import hashlib
import hmac
import os
import sqlite3

ITERACOES = 600_000


def gerar_hash(senha, salt):
    return hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, ITERACOES)


def criar_usuario(conn, usuario, senha):
    salt = os.urandom(16)
    conn.execute(
        "INSERT INTO usuarios (usuario, salt, senha_hash) VALUES (?, ?, ?)",
        (usuario, salt, gerar_hash(senha, salt)),
    )


def criar_banco():
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY, usuario TEXT UNIQUE, salt BLOB, senha_hash BLOB)"
    )
    criar_usuario(conn, "admin", "S3nha-de-lab!")
    criar_usuario(conn, "maria", "outra-senha-de-lab")
    conn.commit()
    return conn


def login(conn, usuario, senha):
    # O "?" separa o comando do dado: o banco nunca interpreta a entrada como SQL.
    linha = conn.execute(
        "SELECT id, usuario, salt, senha_hash FROM usuarios WHERE usuario = ?",
        (usuario,),
    ).fetchone()
    if linha is None:
        return None
    id_usuario, nome, salt, senha_hash = linha
    if hmac.compare_digest(gerar_hash(senha, salt), senha_hash):
        return (id_usuario, nome)
    return None


if __name__ == "__main__":
    conn = criar_banco()
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    resultado = login(conn, usuario, senha)
    if resultado:
        print(f"Bem-vindo, {resultado[1]}!")
    else:
        print("Usuário ou senha inválidos.")

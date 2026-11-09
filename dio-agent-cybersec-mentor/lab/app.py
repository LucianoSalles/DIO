"""Login PROPOSITALMENTE VULNERÁVEL, para estudo em laboratório.

Não use este código em nenhum sistema real.
O banco é criado em memória e some quando o programa termina.
"""

import sqlite3


def criar_banco():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT)")
    conn.execute("INSERT INTO usuarios (usuario, senha) VALUES ('admin', 'S3nha-de-lab!')")
    conn.execute("INSERT INTO usuarios (usuario, senha) VALUES ('maria', 'outra-senha-de-lab')")
    conn.commit()
    return conn


def login(conn, usuario, senha):
    # O SQL é montado juntando o que a pessoa digitou.
    query = (
        "SELECT id, usuario FROM usuarios "
        "WHERE usuario = '" + usuario + "' AND senha = '" + senha + "'"
    )
    return conn.execute(query).fetchone()


if __name__ == "__main__":
    conn = criar_banco()
    usuario = input("Usuário: ")
    senha = input("Senha: ")
    resultado = login(conn, usuario, senha)
    if resultado:
        print(f"Bem-vindo, {resultado[1]}!")
    else:
        print("Usuário ou senha inválidos.")

# Sistema-Web-de-cadastro-de-informa-es-de-pessoas

Um sistema básico em que você cadastra informações de uma pessoa via Web

## Funcionalidade
- Cadastro de clientes com nome, CPF e email
- Listagem de todos os clientes cadastrados
- Exclusão de cadastro

## Tecnologias utilizadas

- Python 3
- SQLite (opcional)
- HTML5 e CSS3

## Comentário: 

1) Para utilizar o sistema primeiro crie um usuário utilizando o código abaixo:

import sqlite3

conn = sqlite3.connect('cadastro.db')
c = conn.cursor()
c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", ("admin", "1234"))
conn.commit()
conn.close()

2) Pode ser facilmente adaptado para outros realidades, como produtos, cadastro de empresas, etc; 

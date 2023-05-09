"""
Este módulo contém funções utilitárias para o projeto.
"""


def process_line(line):
    """
    Processa uma linha e retorna uma lista com os valores separados por
    "\";\"".
    """
    return line.replace("NULL", '"NULL"').strip('"').split('";"')


def busca_binaria_iterativa(users, user_id):
    """
    Retorna a posição do usuário com o ID `user_id` na lista `users`.
    """
    nao_encontrado = None
    limite_inferior = 0
    limite_superior = len(users) - 1

    while limite_inferior <= limite_superior:
        user_pos = limite_inferior + (limite_superior - limite_inferior) // 2
        if users[user_pos]["User-ID"] == user_id:
            if users[user_pos - 1]["User-ID"] != user_id:
                return user_pos
            limite_superior = user_pos - 1
        elif users[user_pos]["User-ID"] < user_id:
            limite_inferior = user_pos + 1
        else:
            limite_superior = user_pos - 1
    if users[user_pos]["User-ID"] == user_id:
        return user_pos

    return nao_encontrado


def get_book_ratings():
    """
    Retorna uma lista com as linhas do arquivo BX-Book-Ratings.csv.
    """
    with open("./assets/BX-Book-Ratings.csv", encoding="iso-8859-1") as file:
        book_ratings = file.read().rstrip("\n")
    book_ratings = book_ratings.split("\n")

    keys = process_line(book_ratings[0])
    book_ratings = list(
        map(
            lambda line: dict(zip(keys, process_line(line))),
            book_ratings[1:],
        )
    )

    return book_ratings


def get_book_ratings_by_isbn(isbn):
    """
    Retorna uma lista de dicionários com as avaliações de um livro.
    """
    ratings = []
    with open("./assets/BX-Book-Ratings.csv", encoding="iso-8859-1") as file:
        keys = process_line(file.readline().rstrip("\n"))
        while line := file.readline().rstrip("\n"):
            if isbn not in line:
                continue
            ratings.append(dict(zip(keys, process_line(line))))
    return ratings

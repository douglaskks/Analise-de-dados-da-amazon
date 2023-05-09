"""
CONSULTA 07
Mostre o livro melhor avaliado por usuários com idade entre X e Y e o número
de avaliações feitas.
"""

import project_utils


def filter_users(data: list, min_age: int, max_age: int) -> list:
    """
    Retorna uma lista com os IDs dos usuários que tem idade entre min_age e
    max_age.
    """
    user_ids = []
    keys = project_utils.process_line(data[0])
    for line in data[1:]:
        user = dict(zip(keys, project_utils.process_line(line)))
        if (
            user["Age"] == "NULL"
            or int(user["Age"]) < min_age
            or int(user["Age"]) > max_age
        ):
            continue
        user_ids.append(user["User-ID"])
    return user_ids


def get_best_rated_book(data, user_ids, minimum_ratings=1):
    """
    Retorna o livro (contido em `data`) melhor avaliado pela lista de usuários
    recebida (`user_ids`).

    `minimum_ratings` é o número mínimo de avaliações que um livro deve ter
    para ser considerado.
    """
    books = {}
    amount = len(user_ids)
    for pos, user_id in enumerate(user_ids):
        print(
            f"""\r{100 * pos//amount:02.0f}% concluído. Aguarde...      """,
            end="",
        )

        pos = project_utils.busca_binaria_iterativa(data, user_id)
        if pos is None:
            continue

        while data[pos]["User-ID"] == user_id:
            books[data[pos]["ISBN"]] = books.get(data[pos]["ISBN"], []) + [
                int(data[pos]["Book-Rating"])
            ]
            pos += 1
        user_ids[user_ids.index(user_id)] = data[pos]

    if minimum_ratings > 1:
        filtered_books = list(
            filter(lambda x: len(books[x]) >= minimum_ratings, books)
        )
        if len(filtered_books) > 0:
            books = {book: books[book] for book in filtered_books}

    best_rated_book = max(books, key=lambda x: sum(books[x]) / len(books[x]))
    print(
        """\r                                                        \r""",
        end="",
    )
    return (
        best_rated_book,
        len(books[best_rated_book]),
        sum(books[best_rated_book]) / len(books[best_rated_book]),
    )


def get_user_data():
    """
    Retorna uma lista com as linhas do arquivo BX-Users.csv.
    """
    with open("./assets/BX-Users.csv", encoding="iso-8859-1") as file:
        user_data = file.read().rstrip("\n")
    user_data = user_data.replace(
        '"275081";"cernusco s\n, milan, italy";NULL',
        '"275081";"cernusco s, milan, italy";NULL',
    ).split("\n")

    return user_data


def main():
    """
    Função principal.
    """
    book_ratings = project_utils.get_book_ratings()
    idade_min = int(input("Digite a idade mínima: "))
    user_data = get_user_data()
    idade_max = int(input("Digite a idade máxima: "))
    # idade_min = 15
    # idade_max = 30

    print("\rFiltrando usuários...", end="")
    user_ids = filter_users(user_data, idade_min, idade_max)
    print("\rPesquisando melhor livro...", end="")
    book_ratings.sort(key=lambda x: int(x["User-ID"]))
    result = get_best_rated_book(book_ratings, user_ids, minimum_ratings=1)

    print(f"O livro melhor avaliado por usuários com idade entre {idade_min}")
    print(f"e {idade_max} é o {result[0]} com {result[1]} avaliações e nota")
    print(f"média igual a {result[2]:.2f}")


if __name__ == "__main__":
    main()

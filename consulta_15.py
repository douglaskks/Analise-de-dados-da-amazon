"""
CONSULTA 15
Mostre o histórico de avaliação de um usuário, exibindo o nome do livro, ISBN,
data de publicação e nome da editora. Também mostre a média de avaliação de
cada livro.
"""

import project_utils


def get_user_data(user_id: str) -> dict:
    """
    Retorna um dicionário com as avaliações de um usuário.
    """
    book_ratings = project_utils.get_book_ratings()
    book_ratings.sort(key=lambda x: int(x["User-ID"]))

    pos = project_utils.busca_binaria_iterativa(book_ratings, user_id)
    if pos is None:
        return None

    user_data = {"User-ID": user_id}
    while book_ratings[pos]["User-ID"] == user_id:
        user_data[book_ratings[pos]["ISBN"]] = int(
            book_ratings[pos]["Book-Rating"]
        )
        pos += 1

    return user_data


def get_rating(isbn):
    """
    Retorna a média de avaliações de um livro.
    """
    ratings = project_utils.get_book_ratings_by_isbn(isbn)
    int_rating_values = []
    for item in ratings:
        int_rating_values.append(int(item["Book-Rating"]))
    return sum(int_rating_values) / len(int_rating_values)


def add_book_data(user_data: dict):
    """
    Adiciona o título, ano de publicação, editora e avaliação média de cada
    livro ao dicionário de entrada.
    """
    if user_data is None:
        return
    with open("./assets/BX_Books.csv", encoding="iso-8859-1") as file:
        books = file.read().rstrip("\n")
    books = books.split("\n")

    keys = project_utils.process_line(books[0])
    books = list(
        map(
            lambda line: dict(zip(keys, project_utils.process_line(line))),
            books[1:],
        )
    )
    if books is None:
        return
    books.sort(key=lambda x: x["ISBN"])

    for book in books:
        if book["ISBN"] in user_data:
            user_data[book["ISBN"]] = {
                "Book-Title": book["Book-Title"],
                "Year-Of-Publication": book["Year-Of-Publication"],
                "Publisher": book["Publisher"],
                "Book-Rating": get_rating(book["ISBN"]),
            }


def print_user_data(user_id: str, user_data: dict) -> None:
    """
    Imprime os dados de um usuário.
    """
    print(f"Usuário: {user_id}")
    for book in user_data:
        if book == "User-ID":
            continue
        print("-----------------------------------------------------------")
        print(f"Livro: {user_data[book]['Book-Title']}")
        print(f"ISBN: {book}")
        print(f"Ano: {user_data[book]['Year-Of-Publication']}")
        print(f"Editora: {user_data[book]['Publisher']}")
        print(f"Avaliação média: {user_data[book]['Book-Rating']:.2f}")
    print("-----------------------------------------------------------")


def main():
    """
    Função principal.
    """
    user_id = input("Digite o ID do usuário: ")
    user_data = get_user_data(user_id)
    if user_data is None:
        print("Usuário não encontrado ou não possui avaliações de livros.")
        return

    add_book_data(user_data)
    print_user_data(user_id, user_data)


if __name__ == "__main__":
    main()

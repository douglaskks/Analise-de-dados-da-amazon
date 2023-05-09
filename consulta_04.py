"""
CONSULTA 04
Mostre o país X que tem a melhor avaliação de um livro Y. Usar o ISBN ou o nome
do livro para realizar a busca.
"""

import project_utils


def is_isbn(text: str) -> bool:
    """
    Verifica se o texto é um ISBN válido.
    """
    return len(text) == 10 and text[:9].isnumeric()


def get_isbn(search_term: str) -> str:
    """
    Retorna o ISBN de um livro a partir do nome do livro.
    """
    search_term = search_term.lower()

    isbn = None
    with open("./assets/BX_Books.csv", encoding="iso-8859-1") as file:
        while line := file.readline().rstrip("\n"):
            parts = line.split(";")
            if parts[1].strip('"').lower() == search_term:
                isbn = parts[0].strip('"')
    return isbn


def get_ratings(isbn: str) -> list:
    """
    Retorna uma lista de dicionários com as avaliações de um livro.
    """
    ratings = project_utils.get_book_ratings_by_isbn(isbn)
    for rating in ratings:
        rating["User-ID"] = int(rating["User-ID"])
    return ratings


def add_user_contries(ratings: list) -> None:
    """
    Adiciona o país de origem do usuário a cada avaliação.
    """
    users = []
    with open("./assets/BX-Users.csv", encoding="iso-8859-1") as file:
        data = file.read().rstrip("\n")
    data = data.replace(
        '"275081";"cernusco s\n, milan, italy";NULL',
        '"275081";"cernusco s, milan, italy";NULL',
    ).split("\n")
    keys = project_utils.process_line(data[0])
    for line in data[1:]:
        user = dict(zip(keys, project_utils.process_line(line)))
        user["User-ID"] = int(user["User-ID"])
        users.append(user)

    for user_rating in ratings:
        pos = project_utils.busca_binaria_iterativa(
            users, user_rating["User-ID"]
        )
        if pos is None:
            ratings.remove(user_rating)
            continue
        user_rating.update(users[pos])
        user_rating["country"] = user_rating["Location"].split(",")[-1].strip()


def get_country_with_max_rating(input_ratings: list) -> str:
    """
    Retorna o país com a maior média de avaliações.
    """
    countries = {}
    for rating in input_ratings:
        countries[rating["country"]] = countries.get(rating["country"], []) + [
            float(rating["Book-Rating"])
        ]
    for country, ratings in countries.items():
        countries[country] = sum(ratings) / len(ratings)
    return max(countries, key=countries.get)


def main():
    """
    Função principal.
    """
    # isbn = "0781434726"
    isbn = input("Escreva o ISBN ou nome exato do livro: ")

    if not is_isbn(isbn):
        isbn = get_isbn(isbn)

    if isbn is None:
        print("Book not found")
        return

    ratings = get_ratings(isbn)
    add_user_contries(ratings)

    country = get_country_with_max_rating(ratings)
    print(f"O país com a melhor avaliação do livro {isbn} é `{country}`.")


if __name__ == "__main__":
    main()

"""
Импортируем все необходимые библиотеки
"""

import json
import sqlite3
import flask

"""
Запускаем работу вьюшек
"""

app = flask.Flask(__name__)

"""
Вьюшка для получения самого свежего фильма по названию
"""

@app.route("/movie/<title>")
def get_movie_by_title(title):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""SELECT `title`, `country`, `release_year`, `listed_in` as `genre`, `description`
                   FROM netflix
                   WHERE `title` LIKE '%{title}%'
                   ORDER BY release_year DESC
                   LIMIT 1
        """
        cursor.execute(query)
        result = cursor.fetchall()
        the_movie = result[0]

        the_movie_dictionary = {
            "title":  the_movie[0],
            "country":  the_movie[1],
            "release_year":  the_movie[2],
            "genre":  the_movie[3],
            "description":  the_movie[4]}
        return flask.jsonify(the_movie_dictionary)


"""
Вьюшка для получения фильмов с 2020 по 2021 год
"""

@app.route("/movie/<int:year1>/to/<int:year2>")
def get_movie_year_to_year(year1, year2):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""SELECT `title`, `release_year`
                      FROM netflix
                      WHERE `release_year` BETWEEN {year1} AND {year2}
                      LIMIT 100
           """
        cursor.execute(query)
        result = cursor.fetchall()
        the_movie = []

        for item in result:
           the_movie.append(item)

        return flask.jsonify(the_movie)

"""
Вьюшка для получения фильма по рейтингу
"""

@app.route("/rating/<rating>")
def get_movie_by_rating(rating):
    dict_by_rating = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""SELECT `title`, `rating`, `description`
                    FROM netflix
                    WHERE `rating` in {dict_by_rating.get(rating, ('PG-13', 'NC-17'))}
            """
        cursor.execute(query)
        result = cursor.fetchall()
        the_movie = []

        for item in result:
            the_movie.append(item)

        return flask.jsonify(the_movie)

"""
Вьюшка для получения фильма по жанру
"""

@app.route("/genre/<genre>")
def get_movie_by_genre(genre):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""SELECT `title`, `description`
                    FROM netflix
                    WHERE `listed_in` LIKE '%{genre.title()}%'
            """
        cursor.execute(query)
        result = cursor.fetchall()
        the_movie = []

        for item in result:
            the_movie.append(item)

        return flask.jsonify(the_movie)

"""
Функция для получения актеров играющих в паре
"""

def get_name_by_actors(name1 = 'Rose McIver', name2 = 'Ben Lamb'):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""SELECT `cast`
                    FROM netflix
                    WHERE `cast` LIKE '%{name1}%' AND `cast` LIKE '%{name2}%'
            """
        cursor.execute(query)
        result = cursor.fetchall()
        main_name = {}

        for item in result:
            names = item.get('cast').split(", ")
            for name in names:
                if name in main_name.keys():
                    main_name[name] += 1
                else:
                    main_name[name] = 1

        result = []
        for item in main_name:
            for item in main_name:
                if item not in (name1, name2) and main_name[item] >= 2:
                    result.append(item)

        return result

"""
Функция для получения фильма или сериала по году выпуска и жанру
"""

def get_movie_by_types_year_genre(types = 'TV Show', release_year = 2021, genre ='TV'):
    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        query = f"""SELECT *
                    FROM netflix
                    WHERE `type` = '{types}'
                    AND `release_year` = '{release_year}'
                    AND `listed_in` LIKE '%{genre}%'
            """
        cursor.execute(query)
        result = cursor.fetchall()
        the_movie = []

        for item in result:
            the_movie.append(item)

        return json.dumps(the_movie)


if __name__ == '__main__':
    app.run(debug=True)

#print(get_movie_by_title("1983"))
#print(run_sql("SELECT * FROM netflix"))

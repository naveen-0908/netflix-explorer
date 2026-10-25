from flask import Flask,jsonify,request,render_template
from sql_connection import get_connection
import mysql.connector
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/movies/search")
def search_movies():
    search_term = request.args.get("title", "")

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT id, title, type, release_year FROM titles where title LIKE %s"""
    cursor.execute(query,(f"%{search_term}%",))
    movies = cursor.fetchall()
    cursor.close()
    connection.close()
    if not movies:
            return jsonify({
                "error":"Not found",
                "message": f"No movie found with title: {search_term}"
            }),404

    return jsonify(movies)

@app.route("/movies/genre/<genre_name>")
def movies_by_genre(genre_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    select title, release_year from titles t join title_genres tg on t.id=tg.title_id join genres g on tg.genre_id = g.id where g.name= %s"""
    cursor.execute(query, (genre_name,))
    movies = cursor.fetchall()

    cursor.close()
    connection.close()
    if not movies:
            return jsonify({
                "error":"Not found",
                "message": f"No movie found with genre: {genre_name}"
            }),404

    return jsonify(movies)

@app.route("/movies/actor/<actor_name>")
def movies_by_actor(actor_name):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    select title, release_year from titles t join title_actors ta on t.id=ta.title_id join actors a on ta.actor_id = a.id where a.name= %s"""
    cursor.execute(query, (actor_name,))
    movies = cursor.fetchall()
    cursor.close()
    connection.close()

    if not movies:
            return jsonify({
                "error":"Not found",
                "message": f"No movie found with actor: {actor_name}"
            }),404

    return jsonify(movies)

@app.route("/movies/year/<int:year>")
def movies_by_year(year):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT id, title, type, release_year FROM titles where release_year = %s"""
    cursor.execute(query, (year,))

    movies = cursor.fetchall()
    cursor.close()
    connection.close()
    if not movies:
            return jsonify({
                "error":"Not found",
                "message": f"No movie found with year: {year}"
            }),404

    return jsonify(movies)

@app.route("/movies/<int:id>")
def movies_by_id(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """select id, title, type, release_year, rating, duration, description from titles where id = %s"""

    cursor.execute(query, (id,))
    movies = cursor.fetchone()

    if not movies:
            return jsonify({
                "error":"Not found",
                "message": f"No movie found with id: {id}"
            }),404

    genre_query = """select g.name from title_genres as tg join genres as g on tg.genre_id = g.id where tg.title_id = %s order by g.name"""
    cursor.execute(genre_query, (id,))
    genre_rows = cursor.fetchall()

    director_query = """select d.name from title_directors as td join directors as d on td.director_id = d.id where td.title_id = %s order by d.name"""
    cursor.execute(director_query, (id,))
    director_rows = cursor.fetchall()

    actorr_query = """select a.name from title_actors as ta join actors as a on ta.actor_id = a.id where ta.title_id = %s order by a.name"""
    cursor.execute(actorr_query, (id,))
    actor_rows = cursor.fetchall()
    cursor.close()
    connection.close()
    

    movies["genres"] = [row["name"] for row in genre_rows]
    movies['directors'] = [row["name"] for row in director_rows]
    movies['actors'] = [row["name"] for row in actor_rows]


    return jsonify([movies]), 200

@app.route("/movies/genres")
def movie_genres():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """select id, name from genres"""

    cursor.execute(query)
    movies = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(movies)

@app.route("/movies/add", methods=['POST'])
def add_movie():
     data = request.get_json(silent=True)

     if not data:
          return (jsonify({
               "error": "Bad Request",
               "message": "Missing or invalid JSON payload"
          }),400,)
     title = data.get("title", "").strip()
     show_id = data.get("show_id", "").strip()
     country = data.get("country", "").strip()
     date_added = data.get("date_added", "").strip()
     release_year = data.get("release_year", "")
     rating = data.get("rating", "").strip()
     duration = data.get("duration", "").strip()
     description = data.get("description", "").strip()
     movie_type = data.get("type", "").strip()

     if not title or not release_year:
          return (jsonify({
               "error":"Unprocessable data",
               "message":"Fields 'title', 'release_year' are required"
          }),400,)
     connection = None
     cursor = None

     try:
          connection = get_connection()
          cursor = connection.cursor(dictionary=True)

          query = """INSERT INTO titles(show_id,title, country, date_added, release_year, rating, duration, description, type)
          values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

          cursor.execute(query,(show_id,title, country, date_added, release_year, rating, duration, description, movie_type))
          connection.commit()

          new_movie_id = cursor.lastrowid
          cursor.close()
          connection.close()
          return jsonify({
               "message":"Movie added successfully",
               "id":new_movie_id,
               "show_id":show_id,
               "title":title,
               "country": country,
               "date_added": date_added,
               "release_year": release_year,
               "rating": rating,
               "duration": duration,
               "description": description,
               "type": movie_type,

          },201,)
     except mysql.connector.Error as db_error:
          print(f"Database insertion failed: {db_error}")
          return jsonify({
               "error":"Database Error",
               "message": "Failed to save the data due to database conflict"
          },500)

@app.route("/movies/update/<int:id>", methods=['PATCH'])
def update_movies(id):
    data = request.get_json(silent=True)
    if not data:
            return (jsonify({
                "error": "Bad Request",
                "message": "Missing or invalid JSON payload"
            }),400)
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """select * from titles where id = %s"""

    cursor.execute(query, (id,))
    movies = cursor.fetchall()
    cursor.close()
    connection.close()
    if not movies:
                return jsonify({
                    "error":"Not found",
                    "message": f"No movie found with id: {id}"
                }),404
    allowed_updates = {"title":"title","date_added":"date_added","rating":"rating","description":"description"}
    update_pairs = []
    query_values = []

    for json_key, db_column in allowed_updates.items():
          if json_key in data:
                value = data[json_key]
                if isinstance(value, str):
                    value  =  value.strip()

                update_pairs.append(f"{db_column} = %s")
                query_values.append(value)

    if not update_pairs:
          return (jsonify({
                "error":"Unprocessable Entity",
                "message":"No valid fields provided for modification",
          }),422)

    query_values.append(id)

    connection = None
    cursor = None
    try:
          connection = get_connection()
          cursor = connection.cursor(dictionary=True)
          query = f"""update titles set {', '.join(update_pairs)} where id = %s"""
          cursor.execute(query, tuple(query_values))
          connection.commit()

          cursor.execute("select * from titles where id = %s", (id,))
          updated_movie = cursor.fetchone()

          return (jsonify({
                "message":"Movie updated successfully",
                "movie":updated_movie,
          },200,))
    except mysql.connector.Error as db_error:
          print(f"Database modification failed")
          return (jsonify({
                "error":"Database error",
                "message":f"Failed to modify due to server side error:{db_error}"
          }),500)

@app.route("/movies/delete/<int:id>",methods=['DELETE'])
def delete_movie(id):
      connection = get_connection()
      cursor = connection.cursor(dictionary=True)

      query = "select * from titles where id = %s"
      cursor.execute(query, (id,))
      movie = cursor.fetchone()
      cursor.close()
      connection.close()


      if not movie:
            return jsonify({
                  "error":"Not found",
                  "message":f"Movie not found with id:{id}"
            }),404

      try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)

            query = "delete from titles where id = %s"
            cursor.execute(query, (id,))
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({
                  "message":f"Movie deleted with id: {id}"
            }),200
      except mysql.connector.Error as db_error:
            print(f"Error while deleting data")
            return jsonify({
                  "Error":"Database Error",
                  "message":f"Delete failed due to server side issue: {db_error}"
            })


@app.route("/movies")
def paginated_movies():
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        sort = request.args.get("sort", "title")
        order = request.args.get("order", "asc")
        type_value = request.args.get("type")
        release_year = request.args.get("release_year")

        conditions = []
        values = []

        if type_value:
             conditions.append("type=%s")
             values.append(type_value)

        if release_year:
             conditions.append("release_year=%s")
             values.append(release_year)

        where_clause = ""

        if conditions:
             where_clause = "where " + " and ".join(conditions)
        print(conditions)
        print(values)
        print(where_clause)
        allowed_sort_cols = {"title":"title","release_year":"release_year"}
        sort_col = allowed_sort_cols.get(sort)
        if not sort_col:
             return jsonify({
                "error": "Invalid sort column",
                "message": "Sort column can only be title or release_year"
             }),400
        order = order.lower()
        if order not in ("asc", "desc"):
             return jsonify({
                  "error":"Invalid order",
                  "message":"Order can only be asc or desc"
             }), 400

        if page < 1: page = 1
        if limit < 1: limit = 10

        if limit > 100 : limit = 100
    except ValueError:
        page = 1
        limit = 10
    offset = (page - 1) * limit
    connection = None
    cursor = None

    try:
          connection = get_connection()
          cursor = connection.cursor(dictionary=True)

          count_query = f"select count(*) as total_count from titles {where_clause}"
          cursor.execute(count_query, tuple(values))
          total_count = cursor.fetchone()['total_count']

          query = f"""select * from titles {where_clause} order by {sort_col} {order} limit %s offset %s"""

          query_values = values + [limit,offset]
          cursor.execute(query, tuple(query_values))

          movies = cursor.fetchall()

          return jsonify({
                "pagination" : {
                      "current_page": page,
                      "per_page": limit,
                      "total_records":total_count,
                      "total_page": (total_count + limit - 1) // limit
                },
                "movies": movies
          }), 200
    except mysql.connector.Error as db_error:
          print(f"Unable to fetch movies")
          return jsonify({
                "Error":"Database Error",
                "message":f"Unable to fetch pagination dataset:{db_error}"
          }),500
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
             connection.close()

@app.route("/movie/<int:movie_id>")
def movie_page(movie_id):
     return render_template(
          "movie_details.html",
          movie_id=movie_id
     )


if __name__ == "__main__":
    app.run(debug=True)
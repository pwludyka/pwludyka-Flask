from flask import *
import sqlite3

app = Flask(__name__)


@app.route("/", methods = ['GET', 'POST'])
def home_page():
    with sqlite3.connect('movies.db') as db:
        cursor = db.cursor()
        if request.method == 'POST':
            movies_to_remove_ids = request.form.getlist('movieToRemove')
            for id in movies_to_remove_ids:
                cursor.execute('DELETE FROM movies where id==?', (id,))
                db.commit()

        cursor.execute('SELECT * FROM movies')
        return render_template('home.html', movies=cursor)

@app.route('/addMovie', methods = ['GET', 'POST'])
def adding_page():
    if request.method == 'POST':
        movieTitle = request.form.get('title')
        movieYear = request.form.get('year')
        movieActors = request.form.get('actors')

        if len(movieTitle)>0 and len(movieYear)>0 and len(movieActors)>0:
            with sqlite3.connect('movies.db') as db:
                db.execute('INSERT INTO movies (title, year, actors) VALUES (?, ?, ?)',
                           (movieTitle, movieYear, movieActors))
                db.commit()
            return redirect(url_for('home_page'))
            

    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
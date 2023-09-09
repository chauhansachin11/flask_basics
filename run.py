from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.update(
    SECRET_KEY='admin',
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:admin@localhost/catalog_db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)


@app.route('/index')
@app.route('/')
def hello_flask():
    return 'Hello Flask !'

@app.route('/new')
def query_string(greeting='hello'):
    query_val = request.args.get('greeting',greeting)
    return '<h1> the greeting is {0} </h1>'.format(query_val)

@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='Sachin'):
    return '<h1> Hello there ! {} </h1>'.format(name)


# NUMBERS
@app.route('/number/<int:num>')
def working_withnumber(num):
    return '<h1> the number you picked is ' + str(num) + '</h1>'


# FLOATS
@app.route('/product/<float:num1>/<float:num2>')
def multiplication(num1,num2):
    return '<h1> the product is {}'.format(num1 * num2) + '</h1>'


@app.route('/sum/<int:num1>/<int:num2>')
def add_two_number(num1,num2):
    return '<h1> the addition is {}'.format(num1 + num2) + '</h1>'


# FROM HTML TEMPLATE
@app.route('/temp')
def use_html_template():
    return render_template('hello.html')


@app.route('/watch')
def top_movies():
    movie_list = ['autopsy of jane doe',
                  'neon demon',
                  'ghost in a shell',
                  'kong: skull island',
                  'john wick 2',
                  'spiderman - homecoming']
    return render_template('movies.html',
                           movies=movie_list,
                           name='Sachin')


@app.route('/tables')
def movies_plus():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}
    return render_template('table_data.html',
                           movies = movies_dict,
                           name = 'Mukul ')


# JINJA2 - FILTERS
@app.route('/filters')
def filter_data():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}

    return render_template('filter_data.html',
                           movies=movies_dict,
                           name=None,
                           film='a christmas carol')

# JINJA2 - MACROS
@app.route('/macros')
def jija_macros():
    movies_dict = {'autopsy of jane doe': 02.14,
                   'neon demon': 3.20,
                   'ghost in a shell': 1.50,
                   'kong: skull island': 3.50,
                   'john wick 2': 02.52,
                   'spiderman - homecoming': 1.48}
    return render_template('using_macros.html',
                           movies=movies_dict)

# PUBLICATION TABLE
class Publication(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'The Publisher is {}'.format(self.name)


# BOOKS TABLE
class Book(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False, index=True)
    author = db.Column(db.String(350))
    avg_rating = db.Column(db.Float)
    format = db.Column(db.String(50))
    image = db.Column(db.String(100), unique=True)
    num_pages = db.Column(db.Integer)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    # ESTABLISH RELATIONSHIP
    pub_id = db.Column(db.Integer, db.ForeignKey('publication.id'))

    def __init__(self, title, author, avg_rating, book_format, image, num_pages, pub_id):

        self.title = title
        self.author = author
        self.avg_rating = avg_rating
        self.format = book_format
        self.image = image
        self.num_pages = num_pages
        self.pub_id = pub_id

    def __repr__(self):
        return '{} by {}'.format(self.title, self.author)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
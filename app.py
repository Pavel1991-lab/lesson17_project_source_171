

from flask import Flask, request
from flask_restx import Api, Resource, Namespace
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

#Создаем схемы
class MovieSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    description = fields.String()
    trailer = fields.String()
    year = fields.Integer()
    rating = fields.Float()
    genre_id = fields.Integer()
    director_id = fields.Integer()

class DirectorSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class GenreSchema(Schema):
    id = fields.Integer()
    name = fields.String()


#Регистрируем namespace
api = Api(app)
movie_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genre_ns = api.namespace('genre')

#Пишем сериализацию модели Movie
#Также реализуем  Moviе через методы POST,GET,PUT
@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id =  request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        movie_schema = MovieSchema(many=True)
        st = Movie.query
        if  director_id:
            st = st.filter(Movie.director_id == director_id)
        if genre_id:
            st = st.filter(Movie.genre_id == genre_id)
        movies = st.all()
        return movie_schema.dump(movies), 200


    def post(self):
        movie_data = request.json
        new_movie = Movie(**movie_data)
        db.session.add(new_movie)
        db.session.commit()
        return '', 201



@movie_ns.route('/<int:uid>')
class MoviesView(Resource):
    def get(self, uid:int):
        movie =  Movie.query.get(uid)
        movie_schema = MovieSchema()
        if not movie:
            return 'Такого фильма нету', 404
        return movie_schema.dump(movie), 200


    def put(self, uid:int):
        movie =  Movie.query.get(uid)
        movie_data = request.json
        movie.title = movie_data.get('title')
        movie.description = movie_data.get('description')
        movie.trailer = movie_data.get('trailer')
        movie.year = movie_data.get('year')
        movie.rating = movie_data.get('rating')
        movie.genre_id = movie_data.get('genre_id')
        movie.director_id = movie_data.get('director_id')
        db.session.add(movie)
        db.session.commit()
        return '', 204

#Пишем сериализацию модели Director
#Также реализуем  Director через методы POST,GET,PUT,DELETE
@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_director = Director.query.all()
        director_schema = DirectorSchema(many = True)
        return director_schema.dumps(all_director), 200


    def post(self):
        director_data = request.json
        new_director = Director(**director_data)
        db.session.add(new_director)
        db.session.commit()
        return '', 201

@directors_ns.route('/<int:uid>')
class DirectorsView(Resource):
    def get(self, uid: int):
        director = Director.query.get(uid)
        director_schema = DirectorSchema()
        if not director:
            return 'Такого директора нету', 404
        return director_schema.dump(director), 200



    def put(self, uid:int):
        director =  Director.query.get(uid)
        director_data = request.json
        director.name = director_data.get('name')
        db.session.add(director)
        db.session.commit()
        return '', 204

    def delete(self, uid: int):
        director = Director.query.get(uid)
        db.session.delete(director)
        db.session.commit()
        return "", 204

#Пишем сериализацию модели Genre
#Также реализуем  Genre через методы POST,GET,PUT,DELETE
@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        all_genre = Genre.query.all()
        genre_schema = GenreSchema(many = True)
        return genre_schema.dumps(all_genre), 200

    def post(self):
        genre_data = request.json
        new_genre = Genre(**genre_data)
        db.session.add(new_genre)
        db.session.commit()
        return '', 201

@genre_ns.route('/<int:uid>')
class GenreView(Resource):
    def get(self, uid: int):
        genre = Genre.query.get(uid)
        genre_schema = GenreSchema()
        if not genre:
            return 'Такого жанра нету', 404
        return genre_schema.dump(genre), 200



    def put(self, uid:int):
        genre = Genre.query.get(uid)
        genre_data = request.json
        genre.name =  genre_data.get('name')
        db.session.add(genre)
        db.session.commit()
        return '', 204

    def delete(self, uid: int):
        genre = Genre.query.get(uid)
        db.session.delete(genre)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)

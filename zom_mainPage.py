import os
from Zom_Forms import  AddForm , DelForm
from flask_restful import Api,Resource
from flask import Flask, render_template, url_for, redirect,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

############################################

        # SQL DATABASE AND MODELS

##########################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)

# class RssFeed(db.Model):
#     __tablename__ = 'rssfeeds'
#     id = db.Column(db.Integer, primary_key=True)
#     url = db.Column(db.String)

class Movies(db.Model):

    __tablename__='movies'
    id=db.Column(db.Integer,primary_key=True)
    movie=db.Column(db.String)
    timing=db.Column(db.String)
    # feed = RssFeed(url='http://url/for/feed')
    #session.add(feed)

    def __init__(self,movie,timing):
        self.movie = movie
        self.timing = timing

    def __repr__(self):
       return f"{self.movie} {self.time} "






class UserBooking(db.Model):

    __tablename__ = 'booking'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    pno=db.Column(db.Integer)
    movie=db.Column(db.Text)
    timing=db.Column(db.String)

    def __init__(self,name,pno,movie,timing):
        self.name = name
        self.pno=pno
        self.movie=movie
        self.timing=timing

    def __repr__(self):
        return f"name: {self.name} "

############################################

        # VIEWS WITH FORMS

##########################################
@app.route('/')
def index():
    mov1_1=Movies('s2','1000')
    mov1_2=Movies('s2','1200')
    mov1_3=Movies('s2','1500')
    mov1_4=Movies('s2','1800')
    mov1_5=Movies('s2','2000')
    mov2_1=Movies('db','1000')
    mov2_2=Movies('db','1200')
    mov2_3=Movies('db','1500')
    mov2_4=Movies('db','1800')
    mov2_5=Movies('db','2000')
    mov3_1=Movies('c2','1000')
    mov3_2=Movies('c2','1200')
    mov3_3=Movies('c2','1500')
    #mov3_4=Movies('c2','1800')
    #mov3_5=Movies('c2','2000')
    db.session.add(mov1_1)
    db.session.add(mov1_2)
    db.session.add(mov1_3)
    db.session.add(mov1_4)
    db.session.add(mov1_5)
    db.session.add(mov2_1)
    db.session.add(mov2_2)
    db.session.add(mov2_3)
    db.session.add(mov2_4)
    db.session.add(mov2_5)
    db.session.add(mov3_1)
    db.session.add(mov3_2)
    db.session.add(mov3_3)
    #db.session.add(mov3_4)
    #db.session.add(mov3_5)
    db.session.commit() 
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()
    form.timing.choices = [(timing.id,timing.timing) for timing in Movies.query.filter_by(movie='s2').all()]
    # if request.method=='POST':

    #     return '<h1>Movies: {form.movie.data},Timing: {form.time.data}</h1>'
    if form.validate_on_submit():
        name = form.name.data
        pno=form.pno.data
        movie=form.movie.data
        timing=form.timing.data

        # Add new Puppy to database
        new_pup = UserBooking(name,pno,movie,timing)
        db.session.add(new_pup)
        db.session.commit()
        return redirect(url_for('list_pup'))

    return render_template('add.html',form=form)

@app.route('/list')
def list_pup():
    # Grab a list of all Movies
    movies =Movies.query.filter_by(movie='S2').all()
    return render_template('list.html', movies=movies)

@app.route('/delete', methods=['GET', 'POST'])
def del_pup():

    form = DelForm()

    if form.validate_on_submit():
        id = form.id.data
        pup = UserBooking.query.get(id)
        db.session.delete(pup)
        db.session.commit()

        return redirect(url_for('list_pup'))
    return render_template('delete.html',form=form)
@app.route('/timing/<movie>')
def timing(movie):
    times=Movies.query.filter_by(movie=movie).all()
    timeArray=[]
    for timings in times:
        timeObj={}
        timeObj['id']=timings.id
        timeObj['timing']=timings.timing
        timeArray.append(timeObj)
    return jsonify({'times' : timeArray})
class MovieResource(Resource):
    def get(self,name,timing):

        mov = Movies.query.filter_by(movie=name,timing=timing).first()

        if mov:
            return mov.json()
        else:
            # If you request a puppy not yet in the puppies list
            return {'name':'not found'}, 404

    def post(self,name,timing):

        newMov = Movies(movie=name,timing=timing)
        db.session.add(newMov)
        db.session.commit()

        return newMov.json()


    def delete(self,name,timing):

        mov =Movies.query.filter_by(name=name,timing=timing).first()
        db.session.delete(mov)
        db.session.commit()

        return {'note':'delete successful'}




class AllMovies(Resource):

    #@jwt_required()
    def get(self):
        # return all the puppies :)
        movies = Movies.query.all()

        # return json of (puppies)
        return [mov.json() for mov in movies]


api.add_resource(MovieResource, '/movie/<string:movie>&<string:timing>')
api.add_resource(AllMovies,'/movies')
if __name__ == '__main__':
           
    
 

    app.run(debug=True)
    
    # pup = UserBooking.query.all()
    # db.session.delete(pup)
    # db.session.commit()

    # pup2=Movies.query.all()
    # db.session.delete(pup2)
    # db.session.commit()



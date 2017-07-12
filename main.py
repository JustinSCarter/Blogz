from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:BlogPass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '6ZEnHDF5MJ'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def index():
    '''displays blog posts on a home page'''

    blogs = Blog.query.all()
    return render_template('blog.html', title='Build a Blog', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def blog_post():
    #creates a new blog object in the database and then returns to the homepage and 
    #returns errors if text inputs left blank and returns input into the inputs
    new_post_title = request.form['']
    new_post_body = request.form['']

    if not new_post_body:

    if not new_post_title:

    


# def add_movie():
#     # look inside the request to figure out what the user typed
#     new_movie_name = request.form['new-movie']

#     # if the user typed nothing at all, redirect and tell them the error
#     if (not new_movie_name) or (new_movie_name.strip() == ""):
#         error = "Please specify the movie you want to add."
#         return redirect("/?error=" + error)

#     # if the user wants to add a terrible movie, redirect and tell them the error
#     if new_movie_name in terrible_movies:
#         error = "Trust me, you don't want to add '{0}' to your Watchlist".format(new_movie_name)
#         return redirect("/?error=" + error)

#     movie = Movie(new_movie_name)
#     db.session.add(movie)
#     db.session.commit()
#     return render_template('add-confirmation.html', movie=movie)

if __name__ == '__main__':
    app.run()
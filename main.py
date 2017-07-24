from flask import Flask, request, render_template, flash, redirect,session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:Final@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '6ZEnHDF5MJ'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Title %r>' % self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    owner_id = request.args.get('owner_id')
    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body)
    if owner_id:
        blogs = Blog.query.filter_by(owner_id=owner_id).all()
        return render_template('SingleUser.html', blogs=blogs)
    blogs = Blog.query.order_by(Blog.id.asc()).all()
    return render_template('blog.html', title='List of all blog posts:', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def new_blog():
    '''Form to create a new blog entry'''
    #add the author of a post to the stored data
    if request.method == 'POST':
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        author = User.query.filter_by(username=session['username']).first()
        if not new_post_body or not new_post_title:
            if not new_post_title:
                flash('A title is required.', 'titleerror')
            if not new_post_body:
                flash('Your post needs some content.', 'bodyerror')
            return render_template('newpost.html', body=new_post_body, title=new_post_title)
        new_post = Blog(new_post_title, new_post_body, author)
        db.session.add(new_post)
        db.session.commit()
        id = new_post.id
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body)

    return render_template('newpost.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()

        if password != verify or existing_user or len(username)<3 or len(password)<3:
            if len(username)<3:
                flash('Please enter a username of at least 3 characters.')
            elif len(password)<3:
                flash('Please enter a password of at least 3 characters.')
            elif password != verify:
                flash('Make sure you type the same password twice.')
            elif existing_user:
                flash('It looks like that user already exists.')
            return render_template('register.html')

        else:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost')

    else:
        return render_template('register.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in!")
            return redirect('/newpost')
        elif not user:
            flash("That user doesn't appear to exist")
            return redirect('/login')
        else:
            flash("That's not the right password")
            return redirect('/login')

    return render_template('login.html')

@app.route('/index')
def index():
    users = User.query.order_by(User.id.desc()).all()
    return render_template('index.html', users=users)

@app.route("/logout")
def logout():
    del session['username']
    return redirect("/blog")

@app.route('/')
def gotoindex():
    '''redirects to /index route'''
    return redirect("/index", code=302)

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'blog', 'index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

app.secret_key = 'M/N_dHktEbgAvL8uqf8Ta3jfZhDvGsYDaK9'

if __name__ == '__main__':
    app.run()

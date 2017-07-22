from flask import Flask, request, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:Final@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '6ZEnHDF5MJ'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.owner = owner

    def __repr__(self):
        return '<Title %r>' % self.title

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.email

@app.route('/blog', methods=['POST', 'GET'])
def index():
    '''displays blog posts on a home page'''
    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body)
    blogs = Blog.query.order_by(Blog.id.desc()).all()
    return render_template('blog.html', title='Build a Blog', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def blog_post():
    '''Form to create a new blog entry'''
    #add the author of a post to the stored data
    if request.method == 'POST':
        new_post_title = request.form['title']
        new_post_body = request.form['body']
        if not new_post_body or not new_post_title:
            if not new_post_title:
                flash('A title is required.', 'titleerror')
            if not new_post_body:
                flash('Your post needs some content.', 'bodyerror')
            return render_template('newpost.html', body=new_post_body, title=new_post_title)
        new_post = Blog(new_post_title, new_post_body)
        db.session.add(new_post)
        db.session.commit()
        id = new_post.id
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body)

    return render_template('newpost.html')

@app.route("/signup", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()

        if not is_email(email):
            flash('Uh-oh! "' + email + '" does not seem like an email address.')
            return redirect('/register')

        if password != verify:
            flash('Make sure you type the same password twice.')
            return redirect('/register')

        if existing_user:
            flash('It looks like that user already exists.')
            return redirect('/register')

        else:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')

    else:
        return render_template('register.html')

def is_email(string):
    # for our purposes, an email string has an '@' followed by a '.'
    # there is an embedded language called 'regular expression' that would crunch this implementation down
    # to a one-liner, but we'll keep it simple:
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()

        if user and user.password == password:
            session['email'] = email
            flash("Logged in!")
            return redirect('/')
        elif not user:
            flash("That user doesn't appear to exist")
            return redirect('/login')
        else:
            flash("That's not the right password")
            return redirect('/login')

    return render_template('login.html')

@app.route('/index')
def index():

@app.route("/logout")
def logout():
    del session['email']
    return redirect("/"):

@app.route('/')
def gotoindex():
    '''redirects to /blog route'''
    return redirect("/blog", code=302)

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login')

app.secret_key = 'M/N_dHktEbgAvL8uqf8Ta3jfZhDvGsYDaK9'

if __name__ == '__main__':
    app.run()

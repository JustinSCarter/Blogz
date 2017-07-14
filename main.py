from flask import Flask, request, render_template, flash, redirect
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

    def __repr__(self):
        return '<Title %r>' % self.title

@app.route('/blog', methods=['POST', 'GET'])
def index():
    '''displays blog posts on a home page'''
    id = request.args.get('id')
    if id:
        blog = Blog.query.filter_by(id=id).first()
        return render_template('blog.html', title=blog.title, body=blog.body)

    blogs = Blog.query.all()
    return render_template('blog.html', title='Build a Blog', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def blog_post():
    '''Form to create a new blog entry'''
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

@app.route('/')
def gotoindex():
    return redirect("/blog", code=302)
if __name__ == '__main__':
    app.run()

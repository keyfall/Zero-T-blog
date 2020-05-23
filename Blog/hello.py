from flask import Flask,render_template,flash,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.sqlite3'
app.secret_key="sdfs"

db = SQLAlchemy(app)

class blogs(db.Model):
    id = db.Column('blog_id',db.Integer,primary_key = True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    keyword = db.Column(db.String(30))
    description = db.Column(db.String(300))
    updatetime = db.Column(db.DateTime)
    see = db.Column(db.Integer,default=0)

    def __init__(self,title,content,keyword,description,updatetime):
        self.title = title
        self.content = content
        self.keyword = keyword
        self.description = description
        self.updatetime = updatetime

db.create_all()




@app.route('/')
def hello_world():
    page = int(request.args.get('page',1))
    per_page = 15
    paginate = blogs.query.order_by(blogs.id.desc()).paginate(page,per_page,error_out=False)
    blogs2 = paginate.items
    return render_template('foreground/home.html',blogs = blogs2,paginate=paginate)

@app.route('/detail')
def detail():
    return render_template('foreground/detail.html')
@app.route('/houtai')
def houtai():

    return render_template('index.html')

@app.route('/article',methods=['GET','PUT','DELETE','POST'])
def article():
    page = int(request.args.get('page',1))    
    per_page = 15
    paginate = blogs.query.order_by(blogs.id.desc()).paginate(page,per_pagen,error_out=False)
    blogs2 = paginate.items
    return render_template("article.html",blogs = blogs2,paginate=paginate)

@app.route('/article/<aid>',methods=['GET','POST','PUT','DELETE'])
def article_id(aid):
    if request.method == 'GET':
        blog = blogs.query.get(aid)
        return render_template('update-article.html',blog = blog)
    elif request.method == "POST":
        if not request.form['title'] or not request.form['content'] \
                or not request.form['keyword'] or not request.form['description'] \
                or not request.form['updatetime']:
                    flash("Please enter all the fields",'error')
        else:
            blog = blogs.query.get(aid)
            blog.title = request.form['title']
            blog.content = request.form['content']
            blog.keyword = request.form['keyword']
            blog.descriptiong= request.form['description']
            blog.updatetime = datetime.strptime(request.form['updatetime'],'%Y-%m-%d').date()
            db.session.commit()
            print('sdfjsiodfjsoifjiosjfoisd')
            return redirect(url_for('article'))
    elif request.method == 'DELETE':
        blog = blogs.query.get(aid)
        db.session.delete(blog)
        db.session.commit()

        return jsonify({'success':'sdfs','abc':'sfsdf'})
    return redirect(url_for('article'))



@app.route('/addarticle',methods=['GET','POST'])
def addarticle():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['content'] \
                or not request.form['keyword'] or not request.form['description'] \
                or not request.form['updatetime']:
                    flash("Please enter all the fields",'error')
        else:
            time = datetime.strptime(request.form['updatetime'],'%Y-%m-%d').date()
            blog = blogs(request.form['title'],request.form['content'],request.form['keyword'],\
                    request.form['description'],time)
            db.session.add(blog)
            db.session.commit()
            return jsonify({'success':'ok','abc':'abcde'})
    return redirect(url_for('article'))



@app.route('/html',methods=['GET','POST'])
def html():
    if request.method == 'POST':
        return redirect(url_for('article'))
    return render_template("add-article.html")













if __name__=='__main__':
    app.run(debug=True)

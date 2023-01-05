from flask import Flask, jsonify
from flask_cors import CORS
from flask import render_template,flash,redirect,url_for,abort,request
from ecommerce.forms import  RegisterForm, LoginForm,PostForm, ContactForm
from werkzeug.security import generate_password_hash


from ecommerce import createApp,db,mail,Message
from ecommerce.models import User,Post
from ecommerce.initialize_db import createDB
from flask_login import  login_user,current_user,logout_user,login_required
from flask_login import LoginManager



# APP AND DB CREATION ---------------------------------------------------------
app = createApp()
CORS(app)
createDB()


@app.route("/")
def index():
    page=request.args.get('page',1,type=int)
    posts=Post.query.order_by(Post.id.desc()).paginate(page=page,per_page=3)
    next_url=url_for('index',page=posts.next_num) if posts.has_next else None
    prev_url=url_for('index',page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html',title='HOME',posts=posts,next_url=next_url,prev_url=prev_url) 

@app.route('/about')

def about():
    return render_template('about.html',title='ABOUT')

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index')) # login islemimiz tamamlanmissa login sayfasina degil index e yönlendirsin

    form=RegisterForm()
    if form.validate_on_submit():
        try:
            name=form.name.data
            brans=dict(form.brans.choices).get(form.brans.data)
            referans_email=form.referans_email.data
            email=form.email.data
            password=form.password.data
            gehashed_pass=generate_password_hash(password)
            checkReferansUser=User.get_user_by_email(referans_email)

            

            if name == None or email == None or password == None or referans_email == None or brans == None or checkReferansUser == None:
                flash(f'{form.referans_email.data} is unvalid as reference email','danger')

           
            User.add_user(name,brans,referans_email,email, password)
            

        except Exception as e:
            print("Error in user add")
            flash(f'Error in Registrierung','danger')
            return redirect(url_for('register',title='REGISTER'))


        flash(f'{form.name.data} account created','success')
        return redirect(url_for('login'))
    

    return render_template('register.html',title='REGISTER',form=form) 

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        try:
            #user3=User.get_user_by_id(19)
            #print(user3)
            user=User.query.filter_by(email=form.email.data).first()
            print("hallo")
            print(user)
            if user and user.password == form.password.data:
                login_user(user)
                flash(f' logged in succesfully','success')
                return redirect(url_for('index'))
            else:
                flash(f' loggin unsuccesfully','danger')
        except Exception as e:
            print("Error in user login")
            print(e)
            return jsonify({"successs": False, "message": str(e)})

    return render_template('login.html',title='LOGIN',form=form) 

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    try:
        if form.validate_on_submit():
            print(current_user)
            print(current_user.id)
            user_id=current_user.id
            title=form.title.data
            subtitle=form.subtitle.data
            post_text=form.post_text.data
            user_id=current_user.id
            post_from=current_user.name
            Post.add_post(title,subtitle,post_text,user_id,post_from)
            flash(f' post created','success')
            return redirect(url_for('index'))
    except Exception as e:
        print(e)
    return render_template('create_post.html',title='Create Post',form=form) 

@app.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',title='post.title',post=post) 

@app.route('/post/<int:post_id>/edit',methods=['GET','POST'])
@login_required
def edit_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form=PostForm()
    
    if form.validate_on_submit():
        post.title=form.title.data
        post.subtitle=form.subtitle.data
        post.post_text=form.post_text.data
        db.session.commit()
        flash(f' post is edited','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.subtitle.data=post.subtitle
        form.post_text.data=post.post_text
        return render_template('create_post.html',title='Edit Post',form=form)

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form=PostForm()
    db.session.delete(post)
    db.session.commit()
    flash(f' post is deleted','success')
    return redirect(url_for('index'))

@app.route('/contact',methods=['GET','POST'])
def contact():
    form=ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            msg=Message(form.name.data, sender='Zero2Heros', recipients=['eyupcoskun.de@gmail.com'])
            msg.body="""
            From:%s
            <%s>
            %s
            """ % (form.email.data, form.phone.data, form.message.data)
            mail.send(msg)
            flash(f' We received your message','success')
            return redirect(url_for('contact'))
        else:
            flash(f' there is an error','danger')
    elif request.method == 'GET':
        return render_template('contact.html',title='Contact',form=form)








    



    
    


if __name__ == "__main__":
    app.run(debug=True)

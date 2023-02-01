from flask import render_template,redirect,session, flash, request
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)



@app.route('/recipes')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    user= User.get_by_id(data)
    return render_template('dashboard.html',user=user, recipes = Recipe.get_all())


@app.route('/recipes/create')
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_recipe.html')

@app.route('/recipes/new', methods=['POST'])
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "user_id" : session['user_id']
    }
    id = Recipe.save(data)
    return redirect('/recipes')


@app.route('/recipe/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("edit.html", recipe =Recipe.get_one_recipe(data))

@app.route('/recipe/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id,
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions']
    }
    print("attempting")
    Recipe.update(data)
    return redirect('/recipes')

@app.route ('/recipe/destroy/<int:id>')
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    Recipe.destroy(data)
    return redirect('/recipes')


@app.route('/recipe/view/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template("recipe.html", recipe = Recipe.get_one_wuser(id))

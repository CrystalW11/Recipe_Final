from flask_app import app, bcrypt
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask import flash, render_template, redirect, request, session


@app.get("/recipes/all")
def all_recipes():
    """This route renders all recipes"""
    
    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipes = Recipe.find_all_with_users()
    user = User.find_by_user_id(session["user_id"])
    return render_template("all_recipes.html", recipes=recipes, user=user)

@app.get("/recipes/new")
def new_recipe():
    """This route displays the new recipe form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])
    return render_template("new_recipe.html", user=user)


@app.post("/recipes/create")
def create_recipe():
    """This route processes the new recipe form."""
    
    if not Recipe.form_is_valid(request.form):
        return redirect("/recipes/new")
    
    # down here the form is valid!!
    Recipe.create(request.form)
    return redirect("/recipes/all")


@app.get("/recipes/dashboard")
def recipes_dashboard():
    """This route displays the user dashboard."""
    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    user = User.find_by_user_id(session["user_id"])

    return render_template("dashboard.html", user=user)


@app.get("/recipes/<int:recipe_id>")
def show_recipe(recipe_id):
    """This route displays one users recipes details"""

    if "user_id" not in session:
        flash("You must be logged in to view the page.", "login")
        return redirect("/")

    recipe = Recipe.find_by_user_id(recipe_id)
    user = User.find_by_user_id(session["user_id"])

    return render_template("show_recipe.html", user=user, recipe=recipe)


@app.get("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    """This route displays the edit recipe form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe = Recipe.find_by_user_id(recipe_id)
    user = User.find_by_user_id(session["user_id"])
    return render_template("edit_recipe.html", recipe=recipe, user=user)


@app.post("/recipes/update")
def update_recipe():
    """This route displays the edit recipe form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    recipe_id = request.form['recipe_id']

    if not Recipe.form_is_valid(request.form):
        return redirect(f"/recipes/{recipe_id}/edit")

    # down here the form is valid
    Recipe.update(request.form)
    return redirect(f"/recipes/{recipe_id}")


@app.get("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    """This route processes the delete form."""

    if "user_id" not in session:
        flash("Please log in.", "login")
        return redirect("/")

    Recipe.delete(recipe_id)
    return redirect('/recipes/all')

from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import recipe
import re
from pprint import pprint
from flask_app.models.user import User
from flask import flash


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

class Recipe:
    """This Recipe class."""

    _db = "recipes_db"

    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.date_cooked = data["date_cooked"]
        self.under_30_min = data["under_30_min"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the recipe form"""
        is_valid = True

        if len(form_data["name"].strip()) == 0:
            flash("Please enter Recipe name.")
            is_valid = False
        elif len(form_data["name"].strip()) < 2:
            flash("Recipe name must be at least two characters.")
            is_valid = False
        if len(form_data["description"].strip()) == 0:
            flash("Please enter Description.")
            is_valid = False
        elif len(form_data["description"].strip()) < 2:
            flash("Description must be at least two characters.")
            is_valid = False
        if len(form_data["instruction"].strip()) == 0:
            flash("Please enter Instructions.")
            is_valid = False
        elif len(form_data["instruction"].strip()) < 2:
            flash("Instructions must be at least two characters.")
            is_valid = False
        if len(form_data["date_cooked"].strip()) == 0:
            flash("Please enter date.")
            is_valid = False
        if len(form_data["under_30_min"].strip()) == 0:
            flash("Please choose Yes or No.")
            is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        """This method finds all the recipes in the database."""

        query = "SELECT * FROM recipes:"
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query)
        pprint(list_of_dicts)
        recipes = []

        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            recipes.append(recipe)

        return recipes

    @classmethod
    def find_all_with_users(cls):
        """This method frinds all the recipes with users in the database. """

        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query)
        recipes = []

        for each_dict in list_of_dicts:
            recipe = Recipe(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            result = User(user_data)
            recipe.user = result
            recipes.append(recipe)

        return recipes

    @classmethod
    def create(cls, form_data):
        """This method creates a recipe from a form."""

        query = """
        INSERT INTO recipes
        (name, description, instruction, date_cooked, under_30_min, user_id)
        VALUES
        (%(name)s, %(description)s, %(instruction)s, %(date_cooked)s, %(under_30_min)s, %(user_id)s);
        """
        recipes_id = connectToMySQL(Recipe._db).query_db(query, form_data)

        return recipes_id

    # @staticmethod
    # def register_form_is_valid(form_data):
    #     """This method validates the registration form."""
    #     print("IN THE VALIDATION METHOD")

    #     is_valid = True

    #     if len(form_data['first_name'].strip()) == 0:
    #         flash("Please enter the first name.", "register")
    #         is_valid = False
    #     elif len(form_data['first_name'].strip()) < 2:
    #         flash("First Name must be at least two characters.")
    #         is_valid = False

    #     if len(form_data['last_name'].strip()) == 0:
    #         flash("Please enter the last name.", "register")
    #         is_valid = False
    #     elif len(form_data['last_name'].strip()) < 2:
    #         flash("Last Name must be at least two characters.")
    #         is_valid = False

    #     if len(form_data['email'].strip()) == 0:
    #         flash("Please enter the email.", "register")
    #         is_valid = False
    #     elif not EMAIL_REGEX.match(form_data['email']):
    #         flash("Email address invalid.", "register")
    #         is_valid = False
    #     if len(form_data['password'].strip()) == 0:
    #         flash("Please enter the password.", "register")
    #         is_valid = False
    #     elif len(form_data["password"].strip()) < 8:
    #         flash("Password must be at least eight characters.", "register")
    #         is_valid = False
    #     elif form_data["password"] != form_data["confirm_password"]:
    #         flash("Passwords do not match.", "register")
    #         is_valid = False

    #     return is_valid

    # @staticmethod
    # def login_form_is_valid(form_data):
    #     """This method validates the login form."""

    #     is_valid = True

    #     if len(form_data['email'].strip()) == 0:
    #         flash("Please enter the email.", "login")
    #         is_valid = False
    #     elif not EMAIL_REGEX.match(form_data['email']):
    #         flash("Email address invalid.", "login")
    #         is_valid = False
    #     if len(form_data['password'].strip()) == 0:
    #         flash("Please enter password.", "login")
    #         is_valid = False
    #     elif len(form_data["password"].strip()) < 8:
    #         flash("Password must be at least eight characters.", "login")
    #         is_valid = False

    #     return is_valid

    # @classmethod
    # def register(cls, recipe_data):
    #     """This method creates a new recipe in the database."""
    #     query = """
    #     INSERT INTO recipes
    #     (name, description, instruction, date_cooked, under_30_min)
    #     VALUES
    #     (%(name)s, %(description)s, %(instruction)s, %(date_cooked)s, %(under_30_min)s);
    #     """

    #     recipe_id = connectToMySQL(Recipe._db).query_db(query, recipe_data)
    #     return recipe_id

    @classmethod
    def find_by_email(cls, email):
        """This method finds a recipe by email."""

        query = """SELECT * FROM recipes WHERE email = %(email)s;"""
        data = {"email": email}
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        recipe = Recipe(list_of_dicts[0])
        return recipe

    @classmethod
    def find_by_recipe_id(cls, recipe_id):
        """This method finds a recipe by recipe_id."""

        query = """SELECT * FROM recipes WHERE id = %(recipe_id)s;"""
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        recipe = Recipe(list_of_dicts[0])
        return recipe

    @classmethod
    def find_by_user_id(cls, recipe_id):
        """This method finds a recipe and the user by the recipe id."""
        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(recipe_id)s;
        """
        data = {"recipe_id": recipe_id}
        list_of_dicts = connectToMySQL(Recipe._db).query_db(query, data)
        pprint(list_of_dicts)
        recipe = Recipe(list_of_dicts[0])
        one_dict = list_of_dicts[0]
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }

        user = User(user_data)
        recipe.user = user
        return recipe

    @classmethod
    def update(cls, form_data):
        """This method updates a recipe in the database."""
        print("\n\n\n\n\line247: ", form_data)
        query = """ 
        UPDATE recipes
        SET name = %(name)s,
        description = %(description)s,
        instruction = %(instruction)s,
        date_cooked = %(date_cooked)s,
        under_30_min = %(under_30_min)s
        WHERE id = %(recipe_id)s;
        """

        connectToMySQL(Recipe._db).query_db(query, form_data)
        return

    @classmethod
    def delete(cls, recipe_id):
        """This method deletes a recipe in the database"""

        query = """
        DELETE FROM recipes
        WHERE id = %(recipe_id)s;
        """
        data = { "recipe_id": recipe_id}
        return connectToMySQL(Recipe._db).query_db(query, data)

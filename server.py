from flask_app import app


# remember to import controllers
from flask_app.controllers import users
from flask_app.controllers import recipes

if __name__ == "__main__":
    app.run(debug=True)

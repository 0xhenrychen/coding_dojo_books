from flask_app import app
from flask_app.controllers import books_controller, authors_controller
from flask_app.models import user, recipe

if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=5004)
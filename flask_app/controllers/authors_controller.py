from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import author, book

@app.route("/")
def index():
    return redirect("/authors")

@app.route("/create_author", methods=["POST"])
def create_author():
    data = {
                "author_name": request.form["author_name"]
    }
    author.Author.save(data)
    return redirect("/authors")

@app.route("/authors")
def authors_all_page():
    authors = author.Author.get_all()
    return render_template("authors.html", authors = authors)

@app.route("/authors/<int:author_id>")
def author_single_page(author_id):
    data = {
                "author_id": author_id
    }
    one_author = author.Author.get_author_by_id(author_id)
    unselected_books = book.Book.get_only_unselected_books(data)
    favorites = book.Book.get_all_book_favs_by_author_join(data)
    return render_template("author.html", author = one_author, books = unselected_books, favorites = favorites)

@app.route("/add_book_favorite", methods=["POST"])
def add_book_to_author():

    data = {
            "author_id": request.form["author_id"],
            "id": request.form["book_id"]
    }
    book.Book.save_book_to_author(data)
    return redirect(f'/authors/{ data["author_id"] }')
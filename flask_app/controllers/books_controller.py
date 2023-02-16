from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import author, book

@app.route("/create_book", methods=["POST"])
def create_book():
    data = {
            "book_name": request.form["book_name"],
            "number_of_pages": request.form["number_of_pages"]
    }
    book.Book.save(data)
    return redirect("/books")

@app.route("/books")
def books_all_page():
    books = book.Book.get_all()
    return render_template("books.html", books = books)

@app.route("/books/<int:book_id>")
def book_single_page(book_id):
    data = {
                "book_id": book_id
    }
    one_book = book.Book.get_book_by_id(data)
    unselected_authors = author.Author.get_only_unselected_authors(data)
    favorites = author.Author.get_all_author_favs_by_book_join(data)
    return render_template("book.html", book = one_book, authors = unselected_authors, favorites = favorites)

@app.route("/add_author_favorite", methods=["POST"])
def add_author_to_book():

    data = {
            "author_id": request.form["author_id"],
            "id": request.form["book_id"]
    }
    author.Author.save_author_to_book(data)
    return redirect(f'/books/{ data["id"] }')
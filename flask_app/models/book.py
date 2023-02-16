from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author
database = "books"

class Book:
    def __init__(self, data):
        self.id = data["id"] # Right side is the name of the MySQL column.
        self.book_name = data["title"]
        self.number_of_pages = data["num_of_pages"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        
    @classmethod
    def save(cls, data):
        query = '''
                    INSERT INTO books (title, num_of_pages)
                    VALUES (%(book_name)s, %(number_of_pages)s);
                '''
        results = connectToMySQL(database).query_db(query, data)
        return results # only return results if you need the ID from the results; otherwise, don't need to return anything.
    
    @classmethod
    def get_all(cls):
        query = '''
                    SELECT * FROM books;
                '''
        results = connectToMySQL(database).query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    @classmethod
    def get_only_unselected_books(cls, data):
        query = '''
                    SELECT * FROM books
                    WHERE books.id NOT IN
                    (SELECT book_id FROM favorites
                    WHERE author_id = %(author_id)s);
                '''
        results = connectToMySQL(database).query_db(query, data)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    @classmethod
    def get_book_by_id(cls, data):
        query = ''' SELECT * FROM books
                    WHERE ID = %(book_id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        return results[0]
    
    @classmethod
    def save_book_to_author(cls, data):
        query = '''
                    INSERT INTO favorites (book_id, author_id)
                    VALUES (%(id)s, %(author_id)s);
                '''
        connectToMySQL(database).query_db(query, data)
    
    @classmethod
    def get_all_book_favs_by_author_join(cls, data):
        query = '''
                    SELECT * FROM favorites
                    JOIN books ON books.id = favorites.book_id
                    JOIN authors ON authors.id = favorites.author_id
                    WHERE favorites.author_id = %(author_id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        output = []
        for row in results:
            this_book = cls(row)
            
            author_data = {
                "id": row["authors.id"],
                "author_name": row["author_name"],
                "created_at": row["authors.created_at"],
                "updated_at": row["authors.updated_at"]
            }
            
            this_book.creator = author.Author(author_data)
            output.append(this_book)
        return output
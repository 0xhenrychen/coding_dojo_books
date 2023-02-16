from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book
database = "books"

class Author:
    def __init__(self, data):
        self.id = data["id"]
        self.author_name = data["author_name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.creator = None
        
    @classmethod
    def save(cls, data):
        query = '''
                    INSERT INTO authors (author_name)
                    VALUES (%(author_name)s);
                '''
        results = connectToMySQL(database).query_db(query, data)
        return results
    
    @classmethod
    def get_all(cls):
        query = '''
                    SELECT * FROM authors;
                '''
        results = connectToMySQL(database).query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors
    
    @classmethod
    def get_only_unselected_authors(cls, data):
        query = '''
                    SELECT * FROM authors
                    WHERE authors.id NOT IN
                    (SELECT author_id FROM favorites
                    WHERE book_id = %(book_id)s);
                '''
        results = connectToMySQL(database).query_db(query, data)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    @classmethod
    def get_author_by_id(cls, id):
        data = {
                "id": id
        }
        query = '''
                SELECT * FROM authors
                WHERE ID = %(id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def save_author_to_book(cls, data):
        query = '''
                    INSERT INTO favorites (author_id, book_id)
                    VALUES (%(author_id)s, %(id)s);
                '''
        connectToMySQL(database).query_db(query, data)
        
    @classmethod
    def get_all_author_favs_by_book_join(cls, data):
        query = '''
                    SELECT * FROM favorites
                    JOIN books ON books.id = favorites.book_id
                    JOIN authors ON authors.id = favorites.author_id
                    WHERE favorites.book_id = %(book_id)s;
                '''
        results = connectToMySQL(database).query_db(query, data)
        output = []
        for row in results:
            this_author = cls(row)
            
            book_data = {
                "id": row["id"],
                "title": row["title"],
                "num_of_pages": row["num_of_pages"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
            this_author.creator = book.Book(book_data)
            output.append(this_author)
        return output
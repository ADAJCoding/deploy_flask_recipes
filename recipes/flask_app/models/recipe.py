from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash


class Recipe:
    db="login_and_register"
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id= data['user_id']
        self.posted_by = None
        
        

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipe (name,description,instructions, user_id) VALUES(%(name)s,%(description)s,%(instructions)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipe JOIN user on recipe.user_id = user.id;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for r in results:
            recipe=cls(r)
            user_data ={
                "id" : r['user.id'],
                "first_name" : r['first_name'],
                "last_name" : r['last_name'],
                "email" : r['email'],
                "password" :"",
                "created_at" : r['user.created_at'],
                "updated_at" : r['user.updated_at']
            }
            recipe.posted_by = user.User(user_data)
            recipes.append(recipe)
        return recipes

    @classmethod
    def get_one_wuser(cls,recipe_id):
        query = "SELECT * FROM recipe JOIN user on recipe.user_id = user.id where recipe.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {"id" :recipe_id})
        print(results[0])
        recipe = cls(results[0])
        user_data ={
                "id" : results[0]['user.id'],
                "first_name" : results[0]['first_name'],
                "last_name" : results[0]['last_name'],
                "email" : results[0]['email'],
                "password" :"",
                "created_at" : results[0]['user.created_at'],
                "updated_at" : results[0]['user.updated_at']
            }
        recipe.posted_by = user.User(user_data) 
        return recipe

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipe WHERE id=%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE recipe SET name=%(name)s, description=%(description)s, instructions=%(instructions)s WHERE id =%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipe WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
        
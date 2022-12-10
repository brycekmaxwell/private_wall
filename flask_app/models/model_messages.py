from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import models_users
from flask_app import app
from flask import flash

class Message:
    DB = "private_wall"
    def __init__(self, data):
        self.id=data["id"]
        self.content=data["content"]
        self.sender=data["sender"]
        self.receiver=data["receiver"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]

    @classmethod
    def get_user_messages(cls, user_id):
        receiver = models_users.User.get_by_id(user_id)
        query = "SELECT messages.*,first_name, last_name, email, senders.created_at as sender_created_at, senders.updated_at as sender_updated_at FROM messages JOIN users as senders on messages.sender_id = senders.id WHERE receiver_id = %(id)s"

        results=connectToMySQL(cls.DB).query_db(query, user_id)

        messages=[]

        for message in results:
            sender_data = {
                "id": message["sender_id"],
                "first_name": message["first_name"],
                "last_name": message["last_name"],
                "email": message["email"],
                "created_at": message["sender_created_at"],
                "updated_at": message["sender_created_at"],
            }
            sender = models_users.User(sender_data)

            message = {
                "id": message["content"],
                "content": message["content"],
                "sender": sender,
                "receiver": receiver,
                "created_at": message["created_at"],
                "updated_at": message["updated_at"],
            }
            messages.append(cls(message))
        return messages

    @classmethod
    def save(cls,data):
        query="INSERT INTO messages (content, sender_id, receiver_id) VALUES (%(content)s, %(sender_id)s, %(receiver_id)s);"
        return connectToMySQL(cls.DB).query_db(query,data)

    @classmethod
    def destroy(cls, message_id):
        query="DELETE FROM messages WHERE message.id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,{"id":message_id})



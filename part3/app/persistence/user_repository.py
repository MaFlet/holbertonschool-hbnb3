from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        # Note that the attribute has an underscore. It seems that getters don't work??
        return super().get_by_attribute("_email", email)
    
# Use these CURL commands for testing
#curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "password123"}'
#curl -X GET "http://127.0.0.1:5000/api/v1/users/<user_id>"
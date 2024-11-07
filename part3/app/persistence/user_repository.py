from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository
from app.persistence import db_session

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Get user by validated email and handling the underscore prefix"""
        return db_session.query(User).filter(User._email == email).first()
    
    def add(self, user_data):
        """Add a new user with attributes"""
        try:
            if isinstance(user_data, dict):
                user = User(
                    first_name = user_data['first_name'],
                    last_name = user_data['last_name'],
                    email = user_data['password'],
                    is_admin = user_data.get('is_admin', False)                
                )
            else:
                user = user_data

            db_session.add(user)
            db_session.commit()
            db_session.refresh(user)
            return user
        except Exception as e:
            db_session.rollback()
            raise ValueError(f"Error adding user: {str(e)}")
        
    def update(self, user_id, user_data):
        """Update user with attributes"""
        user = self.get(user_id)
        if user:
            try:
                if 'first_name' in user_data:
                    user.first_name = user_data['first_name']
                if 'last_name' in user_data:
                    user.last_name = user_data['last_name']
                if 'email' in user_data:
                    user.email = user_data['email']
                if 'password' in user_data:
                    user.password = user_data['password']
                if 'is_admin' in user_data:
                    user.is_admin = user_data['is_admin']
                db_session.commit()
                db_session.refresh(user)
                return user
            except Exception as e:
                db_session.rollback()
                raise ValueError(f"Error updating user: {str(e)}")
            return None
    
# Use these CURL commands for testing
#curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "Jane", "last_name": "Martin", "email": "jane.martine@example.com", "password": "securepassword123"}'
#{
    #"id": "dda62836-478f-4489-9e72-1ae2a5e34fe5",
    #"message": "User created successfully"
#}
#curl -X GET "http://127.0.0.1:5000/api/v1/users/dda62836-478f-4489-9e72-1ae2a5e34fe5"
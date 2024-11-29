from flask_restx import Namespace, Resource, fields, Api, reqparse
# from app.services.facade import HBnBFacade
from app.services.facade import facade
from werkzeug.security import check_password_hash

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

# facade = HBnBFacade()

@api.route('/')
class UserList(Resource):
    @api.expect(user_model)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Setter validation failure')
    def post(self):
        # curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John","last_name": "Doe","email": "john.doe@example.com"}'

        """Register a new user"""
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Validate input data
        if not all([user_data.get('first_name'), user_data.get('last_name'), user_data.get('email'), user_data.get('password')]):
            return {'error': 'Invalid input data'}, 400

        # the try catch is here in case setter validation fails
        new_user = None
        try:
            new_user = facade.create_user(user_data)
        except ValueError as error:
            return { 'error': "Setter validation failure: {}".format(error) }, 400

        return {'id': str(new_user.id), 'message': 'User created successfully'}, 201

    @api.response(200, 'Users list successfully retrieved')
    def get(self):
        """ Get list of all users """
        all_users = facade.get_all_users()
        output = []
        for user in all_users:
            # print(user)
            output.append({
                'id': str(user.id),
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            })

        return output, 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {'id': str(user.id), 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(user_model)
    @api.response(200, 'User details updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """ Update user specified by id """
        try:
            user_data = api.payload
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            allowed_fields = ['first_name', 'last_name', 'email', 'password']
            update_data = {k: v for k, v in user_data.items() if k in allowed_fields}
            if not update_data:
                return {'error': 'No valid fields to update'}, 400
            
            facade.update_user(user_id, update_data)
            updated_user = facade.get_user(user_id)

            return {
                'id': str(updated_user.id),
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'message': 'User updated sucessfully'
            }, 200
        
        except ValueError as error:
            return {'error': f"Validation error: {str(error)}"}, 400
        except Exception as error:
            return {'error': f"Error updating user: {str(error)}"}, 500
        
    @api.response(204, 'User deleted successfully')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user"""
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            facade.delete_user(user_id)
            return '', 204
        except Exception as error:
            return {'error': f"Error deleting user: {str(error)}"}, 500
# LogIn route
users = {
    "user@example.com": {
        "password": "hashed_password"  # This should be a hashed password
    }
}
login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')
@api.route('/login')
class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        email = args['email']
        password = args['password']
        # Check if the user exists and the password is correct
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            # Generate a token (this is just a placeholder)
            token = "your_jwt_token_here"
            return {'message': 'Login successful', 'token': token}, 200
        else:
            return {'message': 'Invalid email or password'}, 401
if __name__ == '__main__':
    app.run(debug=True, port = 5555)

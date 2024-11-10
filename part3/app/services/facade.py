from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
#from app.services.facade import HBnBFacade


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = AmenityRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()

    # In case anyone is curious about the **
    # https://www.geeksforgeeks.org/what-does-the-double-star-operator-mean-in-python/

    # --- Users ---
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    def delete_user(self, user_id):
        """Delete a user"""
        user = self.get_user(user_id)
        if user:
            self.user_repo.delete(user_id)

    # --- Place ---
    def create_place(self, place_data):
        """Create a new place with validation"""
        try:
            owner_id = place_data.get('owner_id')
            if not owner_id:
                raise ValueError("Owner_id is required")
            owner = self.get_user(owner_id)
            if not owner:
                raise ValueError(f"User with id {owner_id} does not exist")
            
            place = Place(
                title = place_data['title'],
                description = place_data['description'],
                price = float(place_data['price']),
                latitude = float(place_data['latitude']),
                longitude = float(place_data['longitude']),
                owner_id = owner_id
            )
            self.place_repo.add(place)
            return place
        except KeyError as e:
            raise Value(f"Missing required field: {(e)}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid data: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error creating place: {str(e)}")
        
    def get_place(self, place_id):
        """Get a place by ID"""
        if not place_id:
            raise ValueError("place_id is required")
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place with validation"""
        try:
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"Place with id {place_id} does not exist")
            if 'owner_id' in place_data:
                new_owner = self.get_user(place_data['owner_id'])
                if not new_owner:
                    raise ValueError(f"User with id {place_data['owner_id']} does not exist")
            self.place_repo.update(place_id, place_data)
            return self.get_place(place_id)
        except Exception as e:
            raise ValueError(f"Error updating place: {str(e)}")

    def get_places_by_owner(self, owner_id):
       """Get all places owned by a user"""
       if not owner_id:
           raise ValueError("owner_id is required")
       owner = self.get_user(owner_id)
       if not owner:
           raise ValueError(f"User with id {owner_id} does not exist")
       return self.place_repo.get_by_owner(owner_id)
    
    def delete_place(self, place_id):
        """Delete a place"""
        place = self.get_place(place_id)
        if place:
            self.place_repo.delete(place_id)

# --- Amenities ---
    # Used during record insertion to prevent duplicate amenities

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
       self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        """Delete an amenity"""
        amenity = self.get_amenity(amenity_id)
        if amenity:
            self.amenity_repo.delete(amenity)


    # # --- Reviews ---
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
       return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
       return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
       self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        self.review_repo.delete(review_id)

facade = HBnBFacade()
__all__ = ['facade']
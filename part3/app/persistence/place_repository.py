from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app.persistence import db_session

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_by_owner(self, owner_id):
        return db_session.query(Place).filter(Place._owner_id == owner_id).all()
    
    def get_with_amenities(self, place_id):
        place = self.get(place_id)
        if place:
            _ = place.amenities
        return place

    def update(self, place_id, data):
        place = self.get(place_id)
        if place:
            try:
                for key, value in data.items():
                    if key == 'title':
                        place.title = value
                    elif key == 'description':
                        place.description = value
                    elif key == 'price':
                        place.price = value
                    elif key == 'latitude':
                        place.latitude = value
                    elif key == 'longitude':
                        place.longitude = value
                    elif key == 'owner_id':
                        place.owner_id = value
                    else:
                        if hasattr(place, key):
                            setattr(place, key, value)
                    db_session.commit()
                    db_session.refresh(place)
                    return place
            except Exception as e:
                db_session.rollback()
                raise ValueError(f"Error updating place: {str(e)}")
            return None
 
# Use these CURL commands for testing
#curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "password123"}'
#curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}'
#curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>""
# curl -X PUT "http://127.0.0.1:5000/api/v1/places/<place_id>" -H "Content-Type: application/json" -d '{"title": "Sunny Apartment", "description": "Great place to stay", "price": 200.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}'
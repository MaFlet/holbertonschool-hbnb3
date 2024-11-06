from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_by_owner(self, owner_id):
        return self.get_by_attribute("_owner_id", owner_id)
    
    #def get_with_amenities(self, place_id):
        #place = self.get(place_id)
        #if place:
            #_ = place.amenities
        #return place

    #def update(self, place_id, data):
        #place = self.get(place_id)
        #if place:
            #for key, value in data.items():
                #if hasattr(place, key):
                    #setattr(place, key, value)
                #self.session.commit()
            #return place
 
# Use these CURL commands for testing
#curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "password": "password123"}'
#curl -X POST "http://127.0.0.1:5000/api/v1/places/" -H "Content-Type: application/json" -d '{"title": "Cozy Apartment", "description": "A nice place to stay", "price": 100.0, "latitude": 37.7749, "longitude": -122.4194, "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}'
#curl -X GET "http://127.0.0.1:5000/api/v1/places/<place_id>""
"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""


import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from datastore import UserRideDataBase
datastores = UserRideDataBase()



class NewRide(messages.Message):
    pickLong = messages.FloatField(1, required=False)
    pickLat = messages.FloatField(2, required=False)
    dropLong = messages.FloatField(3, required=False)
    dropLat = messages.FloatField(4, required=False)
    timeSec = messages.IntegerField(5, required=False)
    daysOfWeek = messages.StringField(6, required=False)
    time = messages.StringField(7, required=False)
    key = messages.IntegerField(9, required=False)
    userID = messages.StringField(8, required=False)
    date = messages.StringField(10, required=False)
    image = messages.StringField(11, required=False)
    pickUp = messages.StringField(12, required=False)
    dropOff = messages.StringField(13, required=False)


class Key(messages.Message):
    key = messages.StringField(1, required=False)


class user(messages.Message):
    userID = messages.StringField(1, required=False)
    rideID = messages.StringField(3, required=False)
    message = messages.StringField(2)

class ReturnRides(messages.Message):
    rides = messages.MessageField(NewRide, 1,repeated=True)


@endpoints.api(name='uberApi', version='v1')
class uberApi(remote.Service):
    """Uber API v1."""
    @endpoints.method(NewRide, Key,
                      path='ride/create', http_method='POST',
                      name='ride.create')  # defines url and type of request
    def create_ride(self, request):
        try:
            key = int(request.key)
        except TypeError:
            key = False
        key = datastores.create_ride_data(request.userID, request.pickLong, request.pickLat, request.dropLong, request.dropLat,
                                          request.timeSec, request.daysOfWeek, request.time, request.date, request.image, key,request.pickUp, request.dropOff)
        return Key(key=str(key.id()))

    @endpoints.method(user, Key,
                      path='user/create', http_method='POST',
                      name='user.create')  # defines url and type of request
    def create_user(self, request):
        key = datastores.creatUser(request.userID, request.message)
        return Key(key=key)

    @endpoints.method(user, Key,
                      path='ride/delete', http_method='POST',
                      name='ride.delete')  # defines url and type of request
    def delete_ride(self, request):
        key = datastores.delete_ride(request.userID, request.rideID)
        return Key(key=key)
    @endpoints.method(user, Key,
                      path='user/create', http_method='POST',
                      name='user.create')  # defines url and type of request
    def create_user(self, request):
        key = datastores.creatUser(request.userID, request.message)
        return Key(key=key)
    @endpoints.method(user, ReturnRides,
                      path='ride/return', http_method='POST',
                      name='ride.return')  # defines url and type of request
    def return_rides(self, request):
        # key = datastores.creatUser(request.userID, request.message)
        return datastores.return_rides(request.userID)






APPLICATION = endpoints.api_server([uberApi])
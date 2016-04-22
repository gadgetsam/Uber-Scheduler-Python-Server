from google.appengine.ext import ndb
import webapp2
import uber_api
class User(ndb.Model):
    """model for representing a user."""
    rides = ndb.IntegerProperty(indexed=False, repeated=True)
    email = ndb.StringProperty(indexed=True)
    # password = ndb.StringProperty(indexed=False)
    # date = ndb.StringProperty(indexed=False, repeated=True)
    
class Ride(ndb.Model):
    """modal for representing a ride"""
    pickLong = ndb.FloatProperty(indexed=False, default=12)
    pickLat = ndb.FloatProperty(indexed=False, default=12)
    dropLong = ndb.FloatProperty(indexed=False, default=12)
    dropLat = ndb.FloatProperty(indexed=False, default=12)
    dropOff = ndb.StringProperty(indexed=False, default="test")
    pickUp = ndb.StringProperty(indexed=False, default="test")
    timeSec = ndb.IntegerProperty(indexed=False, default=12)
    time = ndb.StringProperty(indexed=False, default="test")
    daysOfWeek = ndb.StringProperty(indexed=False, default="test")
    date = ndb.StringProperty(indexed=False, default="test")
    image = ndb.StringProperty(indexed=False, default="test")

    def rideQuery(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)

class UserRideDataBase(webapp2.RequestHandler):
    def creatUser(self, userID, email):
        try:
            user = ndb.Key('User', userID).get().rides
            return "success"
        except AttributeError:

            print "Creating user"


            user = User(email=email, id=userID)
            user.put()


            return "success"
        return "user fail"

    def create_ride_data(self, userID, pickLong, pickLat, dropLong, dropLat, timeSec, daysOfWeek, time, date, image, rideID, pickUp, dropOff):
        if(rideID != False):
            ride = ndb.Key('User', userID, 'Ride', int(rideID)).delete()
        user = ndb.Key('User', userID).get()


        newRide = Ride(pickLong=pickLong, pickLat=pickLat, dropLong=dropLong, dropLat=dropLat, timeSec=timeSec,
                       daysOfWeek=daysOfWeek, time=time, parent=ndb.Key('User', userID), date=date, image=image,
                       pickUp=pickUp, dropOff=dropOff)
        key =newRide.put()
        user.rides.append(key.id())
        user.put()
        return key
    def return_rides(self, userID):
        user = ndb.Key('User', userID).get()
        rideKey = []
        x = 5
        rides = []
        try:
            rideKey = user.rides
        except:
            return uber_api.ReturnRides()
        for rideID in rideKey:
            ride = ndb.Key('User', userID, 'Ride', rideID).get()
            try:
                newRide = uber_api.NewRide(pickLong=ride.pickLong, pickLat=ride.pickLat, dropLong=ride.dropLong, dropLat=ride.dropLat,
                        timeSec=ride.timeSec, daysOfWeek=ride.daysOfWeek, time=ride.time, key=rideID, date=ride.date,
                        image=ride.image,pickUp=ride.pickUp, dropOff=ride.dropOff)
                rides.append(newRide)
            except AttributeError:
                x ="test"
        return uber_api.ReturnRides(rides=rides)
    def delete_ride(self, userID, rideID):
        ride = ndb.Key('User', userID, 'Ride', int(rideID)).delete()
        user =ndb.Key('User', userID).rides.remove(rideID)
        user.put()
        return "success"
    def update_ride(self, userID, rideID):
        ride = ndb.Key('User', userID, 'Ride', int(rideID)).delete()
        user =ndb.Key('User', userID).rides.remove(rideID)
        user.put()
        return "success"




    # def create_ride(self, userID, pickLong, pickLat, dropLong, dropLat, timeSec, daysOfWeek, time):
    #     user = ndb.Key('User', userID).get()




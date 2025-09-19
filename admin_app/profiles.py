import mongoengine as me
from django.conf import settings

me.connect(host=settings.MONGODB_URI)

class UserProfile(me.Document):
    user_id = me.IntField(required=True, unique=True)
    name = me.StringField(max_length=50)
    address = me.StringField(max_length=255)
    points = me.IntField(default=0)
    status = me.BooleanField(default=True)

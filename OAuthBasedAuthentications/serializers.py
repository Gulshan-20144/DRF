from rest_framework import serializers
from SerializersApp.models import BookStore,Books
from user.models import User
class OAuthSerializers(serializers.ModelSerializer):
    class Meta:
        model=BookStore
        fields=["id","name","user","books","Qty"]
        extra_kwargs={
                  "user":{"required":True,"allow_null":False},
                  "name":{"required":True,"allow_null":False},
                  "books":{"required":True,"allow_null":False}
                }
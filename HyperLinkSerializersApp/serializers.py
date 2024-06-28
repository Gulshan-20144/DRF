from rest_framework import serializers
from SerializersApp.models import BookStore, Books
from user.models import User

class BuyBooksHyperSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="bookstore-detail")
    user = serializers.HyperlinkedRelatedField(view_name="bookstore-detail", read_only=True)
    books = serializers.HyperlinkedRelatedField(view_name="bookstore-detail", read_only=True)

    class Meta:
        model = BookStore
        fields = ["url", 'id', "name", "user", "books", "Qty"]
        extra_kwargs={
                  "user":{"required":True,"allow_null":False},
                  "name":{"required":True,"allow_null":False},
                  "books":{"required":True,"allow_null":False}
                }
                
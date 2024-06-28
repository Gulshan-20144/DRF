from rest_framework import serializers
from SerializersApp.models import BookStore,Books
from user.models import User


class CustomSerializer(serializers.ModelSerializer):
    class Meta:
        model=BookStore
        fields=["id","name","user","books","Qty"]
        extra_kwargs={
                  "user":{"required":True,"allow_null":False},
                  "name":{"required":True,"allow_null":False},
                  "books":{"required":True,"allow_null":False}
                }


class BuyBooksListSerializer(serializers.ListSerializer):
    
    child=CustomSerializer()
    
    # def to_internal_value(self, attrs):
    #     print(attrs,"fgdffggf")
    #     user=User.objects.filter(email=attrs.pop("user")).first()
    #     attrs["user"]=user
    #     if not user:
    #         raise serializers.ValidationError("this User Not Exist")
    #     book=Books.objects.filter(id=attrs.pop("books")).first()
    #     attrs["books"]=book
    #     if not book:
    #         return serializers.ValidationError("this Not Available")
    #     return attrs
    
    def create(self, validated_data):
        book_stores = [BookStore(**item) for item in validated_data]
        return BookStore.objects.bulk_create(book_stores)

    def update(self, instance, validated_data):
        # Check if validated_data is a single list, convert to list if necessary
        if isinstance(validated_data, list):
            for validated_datas in validated_data:
                validated_datas = validated_datas

        for id, data in validated_datas.items():
                setattr(instance, id, data)
                instance.save()

        return instance


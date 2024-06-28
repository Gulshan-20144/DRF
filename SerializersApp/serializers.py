from rest_framework import serializers
from .models import BookStore,Books
from user.models import User
class BuyBooksSerializer(serializers.Serializer):
    name=serializers.CharField(required=True,allow_null=False)
    user=serializers.EmailField(required=True,allow_null=False)
    books=serializers.IntegerField(required=True,allow_null=False)
    Qty=serializers.IntegerField(required=True,allow_null=False)

    class Meta:
        model=BookStore
        fields=["name","user","books","Qty"]

    def validate(self, attrs):
        user=User.objects.using("default").filter(email=attrs.pop("user")).first()
        attrs["user"]=user
        if not user:
            raise serializers.ValidationError("this User Not Exist")
        book=Books.objects.using("default").filter(id=attrs.pop("books")).first()
        attrs["books"]=book
        if not book:
            return serializers.ValidationError("this Not Available")
        return attrs
    
    def create(self, validated_data):
        user=BookStore.objects.using("default").create(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        user=BookStore.objects.using("default").filter(id=instance.id).first()
        user.name=validated_data["name"]
        user.user=validated_data["user"]
        user.books=validated_data["books"]
        user.save()
        return user
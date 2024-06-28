from rest_framework import serializers
from user.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import Group
from django.db import transaction


class RagisterSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,allow_null=False)
    first_name=serializers.CharField(required=True,allow_null=False)
    class Meta:
        model=User
        fields=['email',"first_name","last_name","contact","gender","dob","password"]
    extra_kwargs={
                  "password":{"write_only":True,"allow_null":False},
                  "email":{"required":True,"allow_null":False},
                  "contact":{"required":True,"allow_null":False}
                }
    
    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.using("default").filter(email=validated_data.get("email"))
        if user.exists():
            raise serializers.ValidationError({"error": "This user already exists"})
        
        # Corrected line: call create_user on the model manager
        user = User.objects.db_manager("default").create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )      
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.contact = validated_data["contact"]
        user.gender = validated_data["gender"]
        user.dob = validated_data["dob"]
        user.groups.add(Group.objects.db_manager("default").get(name="User"))
        user.save()
        
        return user
    # @transaction.atomic
    # def create(self, validated_data):

    #     user=User.objects.using("default").filter(email=validated_data.get("email"))
    #     print(user,"dddddddddd")
    #     if user.exists():
    #         raise serializers.ValidationError({"error":"this user already exists"})
    #     user=User.objects.using("default").create_user(email=validated_data["email"],password=validated_data["password"])
    #     user.first_name=validated_data["first_name"]
    #     user.last_name=validated_data["last_name"]
    #     user.contact=validated_data["contact"]
    #     user.gender=validated_data["gender"]
    #     user.dob=validated_data["dob"]
    #     user.groups.add(Group.objects.using("default").get(name="User"))
    #     user.save()
    #     return object

class LoginTokenSerializers(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls,user):
        token=super(LoginTokenSerializers,cls).get_token(user)
        return token
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password=serializers.CharField(required=True,allow_null=False)
    password=serializers.CharField(required=True,allow_null=False)
    confirm_password=serializers.CharField(required=True,allow_null=False)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Both password is not same")
        return attrs
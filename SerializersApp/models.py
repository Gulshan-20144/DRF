from django.db import models
from user.models import User
# Create your models here.
class Books(models.Model):
    name=models.CharField(max_length=400,)
    author_name=models.CharField(max_length=400)
    class Meta:
        app_label = 'SerializersApp'


class BookStore(models.Model):
    name=models.CharField(max_length=100)
    user=models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    books=models.OneToOneField(Books, on_delete=models.CASCADE,blank=True,null=True)
    Qty=models.IntegerField(blank=True,null=True)
    is_deleted=models.BooleanField(default=False)
    created_on=models.DateField(auto_now=True)
    updated_on=models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        app_label='SerializersApp'

class UserBlock(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    system_ip = models.GenericIPAddressField()
    timestamps = models.DateTimeField(null=False, blank=False)
    count_num=models.IntegerField(null=False,blank=False)

    def __str__(self):
        return f"{self.user.email} - {self.system_ip}"
    
    class Meta:
        app_label='SerializersApp'
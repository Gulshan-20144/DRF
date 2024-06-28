from django.db import models
# Create your models here.
class Distibuter(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    age=models.IntegerField(null=True)
    address=models.CharField(max_length=150,null=True,blank=True)
    pincode=models.CharField(max_length=6,null=False,blank=False)
    doc_number=models.CharField(max_length=20,null=False,blank=False)

    def __str__(self) -> str:
        return self.name
    class Meta:
        app_label='RouterApp'
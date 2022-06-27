from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Client(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return (self.first_name + " " + self.last_name)
        

class Transaction(models.Model):
    transferFrom =models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, related_name='transferFrom')
    transferTo =models.ForeignKey(Client,on_delete=models.SET_NULL, null=True, related_name='transferTo')
    amount= models.IntegerField()
    title= models.CharField(max_length=200)
    created =models.DateTimeField(auto_now_add=True)


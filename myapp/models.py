from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Area(models.Model):
    Area=models.CharField(max_length=50)
    District=models.CharField(max_length=50)
    Place=models.CharField(max_length=50)
    Pin=models.CharField(max_length=10)
    Post=models.CharField(max_length=30)

class Pickup(models.Model):
    Name = models.CharField(max_length=50)
    Logo = models.CharField(max_length=800)
    Email = models.CharField(max_length=40)
    Phone = models.CharField(max_length=10)
    Tagline = models.CharField(max_length=50)
    Status = models.CharField(max_length=50)
    Latitude = models.CharField(max_length=50)
    Longitude = models.CharField(max_length=50)
    AUTHUSER=models.OneToOneField(User,on_delete=models.CASCADE)
    AREA=models.ForeignKey(Area,on_delete=models.CASCADE)

class Users(models.Model):
    Name = models.CharField(max_length=50)
    Photo = models.CharField(max_length=800)
    Email = models.CharField(max_length=50)
    Number = models.CharField(max_length=10)
    DOB = models.DateField()
    Gender = models.CharField(max_length=10)
    AUTHUSER = models.OneToOneField(User, on_delete=models.CASCADE)
    AREA = models.ForeignKey(Area, on_delete=models.CASCADE)


class Subarea(models.Model):
    Subarea = models.CharField(max_length=50)
    AREA = models.ForeignKey(Area, on_delete=models.CASCADE)
    PICKUP = models.ForeignKey(Pickup, on_delete=models.CASCADE,default='1')


class Staff(models.Model):
    Name = models.CharField(max_length=50)
    Photo = models.CharField(max_length=800)
    License = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Number = models.CharField(max_length=10)
    DOB = models.DateField()
    Gender = models.CharField(max_length=10)
    SUBAREA=models.ForeignKey(Subarea, on_delete=models.CASCADE)
    AUTHUSER = models.OneToOneField(User, on_delete=models.CASCADE)


class Complaint(models.Model):
    Date = models.DateField()
    Complaint = models.CharField(max_length=1000)
    Reply = models.CharField(max_length=1000)
    Status = models.CharField(max_length=20)
    USERS=models.ForeignKey(Users,on_delete=models.CASCADE)


class Feedback(models.Model):
    Date = models.DateField()
    Feedback = models.CharField(max_length=1000)
    Rating = models.CharField(max_length=400)
    USERS = models.ForeignKey(Users, on_delete=models.CASCADE)
    STAFF= models.ForeignKey(Staff, on_delete=models.CASCADE)


class Category(models.Model):
    Category = models.CharField(max_length=50)
    Type = models.CharField(max_length=50)
    Price = models.CharField(max_length=10)


class WasteRequest(models.Model):
    Date = models.DateField()
    Status = models.CharField(max_length=80)
    Latitude = models.CharField(max_length=80)
    Longitude = models.CharField(max_length=80)
    USERS = models.ForeignKey(Users, on_delete=models.CASCADE)
    CATEGORY = models.ForeignKey(Category, on_delete=models.CASCADE)
    PICKUP = models.ForeignKey(Pickup, on_delete=models.CASCADE)



class AssignStaff(models.Model):
    Date= models.DateField()
    Status = models.CharField(max_length=20)
    WASTEREQ = models.ForeignKey(WasteRequest, on_delete=models.CASCADE)
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)



class Chat(models.Model):
    Date = models.DateField()
    Message = models.CharField(max_length=1000)
    FROMUSER=models.ForeignKey(User, on_delete=models.CASCADE,related_name='fromid')
    TOUSER=models.ForeignKey(User, on_delete=models.CASCADE,related_name='toid')



class Payment(models.Model):
    Date = models.DateField()
    Status = models.CharField(max_length=20)
    amount= models.IntegerField()

    WASTEREQ = models.ForeignKey(WasteRequest, on_delete=models.CASCADE)


class Bill(models.Model):
    Bill = models.CharField(max_length=50)
    WASTEREQ = models.ForeignKey(WasteRequest, on_delete=models.CASCADE)















from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


# Create Wing model
class Wing(models.Model):
    wing_name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.wing_name
    


# Create Flat model
class Flat(models.Model):
    flat_num = models.IntegerField()
    wing_name = models.ForeignKey(Wing, on_delete=models.CASCADE, related_name='flat')

    def __str__(self):
        return str(self.flat_num)+' - '+self.wing_name.wing_name
    

# Create Member model
class Member(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    address = models.TextField(max_length=100)
    marritial_status = models.CharField(max_length=10)
    profession = models.CharField(max_length=30)
    isAdmin = models.BooleanField(default=False)
    family_members = models.TextField(max_length=80,blank=True, null=True)
    wing = models.OneToOneField(Wing, blank=True, null=True, on_delete=models.CASCADE)
    flat = models.OneToOneField(Flat, blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Create CustomeUser model
class CustomeUser(AbstractUser):
    contact_num = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    address = models.TextField(max_length=100)
    marritial_status = models.CharField(max_length=10)
    profession = models.CharField(max_length=30)
    isAdmin = models.BooleanField(default=False)
    family_members = models.TextField(max_length=80,blank=True, null=True)
    wing = models.OneToOneField(Wing, blank=True, null=True, on_delete=models.CASCADE)
    flat = models.OneToOneField(Flat, blank=True, null=True,on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()


# Create Society model
class Society(models.Model):
    society_name = models.CharField(max_length=100)
    secretary = models.OneToOneField(CustomeUser, on_delete=models.PROTECT)

    def __str__(self):
        return self.society_name

# Create Issue model
class Issue(models.Model):
    member = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name='user')
    heading = models.CharField(max_length=70, blank=False, null=False)
    description = models.TextField()
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE, related_name='wing',default=0)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='flat', default=0)
    status = models.CharField(max_length=30, blank=True, null=True)
    pcd = models.DateTimeField(default=timezone.now())
    prd = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.member.name+' - '+self.heading


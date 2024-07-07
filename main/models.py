from django.db import models
from django.contrib.auth.models import User

# Create Society model
class Society(models.Model):
    society_name = models.CharField(max_length=100)
    secretary = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.society_name



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
        return self.flat_num+' - '+self.wing_name
    

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
    family_members = models.TextField(max_length=80,blank=True, null=True)
    wing = models.OneToOneField(Wing, blank=True, null=True, on_delete=models.CASCADE)
    flat = models.OneToOneField(Flat, blank=True, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


# Create Issue model
class Issue(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='issues')
    heading = models.CharField(max_length=70, blank=False, null=False)
    description = models.TextField()

    def __str__(self):
        return self.member.name+' - '+self.heading


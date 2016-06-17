from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def user_directory_path(instance, filename):
    return 'quicktutorsApp/user_directory/user_{0}/{1}'.format(instance.user.id, filename)

def reunionSite_directory_path(self,filename):
    return 'quicktutorsApp/reunion_site_directory/{0}'.format(filename)

def university_directory_path(self,filename):
    return 'quicktutorsApp/university_directory/{0}'.format(filename)

class Area(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Career(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class ReunionSite(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=reunionSite_directory_path, default='reunion_site_directory/no-image.jpg')
    address = models.TextField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class University(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to=university_directory_path, default='university_directory/no-img.jpg')
    reunion_sites = models.ManyToManyField(ReunionSite, default='')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    area = models.ForeignKey(Area, default='')
    description = models.TextField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(max_length=500, null=True, blank=True)
    studentID = models.CharField(max_length=10)
    picture = models.ImageField(upload_to=user_directory_path, default='pic_folder/None/no-img.jpg')
    career = models.ForeignKey(Career, default='')
    university = models.ForeignKey(University, default='')
    subjects = models.ManyToManyField(Subject, default='')
    video = models.URLField(null=True, blank=True)
    begin_time = models.TimeField()
    end_time = models.TimeField

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)


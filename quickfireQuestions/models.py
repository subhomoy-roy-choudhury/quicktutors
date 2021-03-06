from django.db import models
from django.utils import timezone
from user_profile.models import Subject
from django.contrib.auth.models import User
# Create your models here.


# Question Model
class Question(models.Model):
    isAnswered = models.BooleanField(default=False)
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, null=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title


# Comment Model
class Comment(models.Model):
    question = models.ForeignKey('quickfireQuestions.Question', related_name='comments')
    author = models.ForeignKey(User)
    text = models.TextField()
    isCorrectAnswer = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text



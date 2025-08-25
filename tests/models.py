from django.db import models

class User(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='user', null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    def __str__(self):
        return self.username
class Category(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name
class Group(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    admin = models.ForeignKey('User', on_delete=models.CASCADE)
    pin = models.IntegerField()
    code = models.CharField()
    def __str__(self):
        return self.name

class Questions(models.Model):
    question = models.CharField(max_length=100)
    file = models.FileField(upload_to='questions')
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    def __str__(self):
        return self.group_id.name

class Answer(models.Model):
    question = models.ForeignKey('Questions', on_delete=models.CASCADE)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return self.question.group_id.name

class Result(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)
    ball = models.IntegerField()

    def __str__(self):
        return self.user.username
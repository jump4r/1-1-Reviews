from django.db import models

# Create your models here.

class Post(models.Model):
    user = models.CharField(max_length=32)
    date = models.IntegerField()
    link = models.CharField(max_length=50)
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title + ', ' + self.user

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.CharField(max_length=32)
    date = models.IntegerField()
    itemName = models.CharField(max_length=32)
    itemLink = models.CharField(max_length=50)
    itemReview = models.CharField(max_length=250)
    itemSize = models.CharField(max_length=32)

    def __str__(self):
        return self.itemName + ', by ' + self.user
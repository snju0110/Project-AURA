from django.db import models


# Create your models here.

class demDatatable(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    amount = models.IntegerField()
    sentFrom = models.CharField(max_length=200)
    sentTo = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    primaryCat = models.CharField(max_length=200)
    groupCat = models.CharField(max_length=200)

    def __str__(self):
        return self.user


class demDailyData(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    user = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    amount = models.IntegerField()
    sentFrom = models.CharField(max_length=200)
    sentTo = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    primaryCat = models.CharField(max_length=200)
    groupCat = models.CharField(max_length=200)

    def __str__(self):
        unique_together = ["date", "user", "amount", "sentFrom", "sentTo"]
        return self.user

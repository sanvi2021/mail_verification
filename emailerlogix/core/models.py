from django.db import models

# Create your models here.
class SingleEmaillist(models.Model):
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)


class Account_Balance(models.Model):
    initial_balance = models.IntegerField(default=1000)

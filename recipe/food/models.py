from django.db import models
import datetime
from django.utils import timezone

class Food(models.Model):
    con_name = models.CharField(max_length = 50)
    rec_name = models.CharField(max_length = 50,unique = True)
    no_of_items = models.IntegerField(default=2)
    cuisine_name = models.CharField(max_length = 50)
    pub_date = models.DateTimeField('date published')
    procedure = models.FileField(upload_to='food/procedure/')
    def __str__(self):
        return self.rec_name
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Recipes(models.Model):
    rec_name = models.ForeignKey('Food', on_delete=models.CASCADE,default=0)
    item = models.CharField(max_length = 50)
    quantity = models.CharField(max_length = 100)

    def __str__(self):
        return self.item

from django.db import models
# from adaptor.model import CsvModel

# Create your models here.
class Data1(models.Model):
    xdata = models.FloatField()
    ydata = models.FloatField()

# class Data2(CsvModel):
#     xdata = models.FloatField()
#     ydata = models.FloatField()

#     class Meta:
#     	delimiter = ","
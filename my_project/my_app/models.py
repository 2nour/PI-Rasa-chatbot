from django.db import models

# Create your models here.
class auth(models.Model):
    id= models.AutoField(primary_key=True)
    login = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=50,default='')
    id_active = models.IntegerField(null=True)

    def __str__(self):
        return self.username



    emp_Auth = models.Manager()

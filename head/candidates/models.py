from django.db import models

# Create your models here.
class Candidate(models.Model):
    tse_id = models.IntegerField(db_index=True, unique=True)
    name = models.CharField(max_length=255)
    number = models.IntegerField()
    party = models.CharField(max_length=20, null=True)
    electoral_unit = models.CharField(max_length=2, null=True)

    def __str__(self) :
        return self.name
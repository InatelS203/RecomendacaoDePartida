from django.db import models

# Create your models here.


class player(models.Model):
    nome = models.CharField(max_length=100),
    id = models.AutoField(primary_key=True),
    rank = models.IntegerField(),
    
    def __str__(self):
        return self.nome, self.id, self.rank
            



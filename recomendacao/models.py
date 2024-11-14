from django.db import models

# Create your models here.


class player(models.Model):
    nome = models.CharField(max_length=10,default="Usuario")
    id = models.AutoField(primary_key=True)
    rank = models.IntegerField(default=0)
    
    def __str__(self):
        return self.nome, self.id, self.rank
            
class partida(models.Model):
    player = models.ForeignKey(player,on_delete=models.CASCADE)
    complete = models.BooleanField()
    text= models.CharField(max_length=300)

    def __str__(self):
        return self.text
    

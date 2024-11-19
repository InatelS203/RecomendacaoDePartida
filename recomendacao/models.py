from django.db import models
from django.utils.timezone import now
from datetime import datetime, timedelta

class Rank(models.Model):
    nome = models.CharField(max_length=20)
    intervalo_minimo = models.IntegerField()
    intervalo_maximo = models.IntegerField()

    def __str__(self):
        return f"{self.nome} ({self.intervalo_minimo}-{self.intervalo_maximo})"


class Localizacao(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Player(models.Model):
    nome = models.CharField(max_length=15, default="Usuario")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    mmr = models.IntegerField(default=0, verbose_name="MMR")  # Valor do rank do player
    toxicidade = models.FloatField(default=10.0, verbose_name="Toxicidade")  # Quanto mais baixo, mais tóxico
    localizacao = models.ForeignKey(Localizacao, on_delete=models.CASCADE)
    recompensa = models.FloatField(default=0.0, verbose_name="Recompensa")  # Recompensa extra ao vencer
    tempo_procura = models.TimeField(verbose_name="Tempo de Procura")  # Tempo em que começou a buscar partida

    def __str__(self):
        return f"{self.nome} (ID: {self.id}, Rank: {self.rank}, MMR: {self.mmr})"

    def tempo_espera(self) -> float:
        """
        Calcula o tempo de espera do jogador em minutos.
        """
        now_time = now().time()
        tempo_inicio = datetime.combine(datetime.today(), self.tempo_procura)
        tempo_atual = datetime.combine(datetime.today(), now_time)

        if tempo_atual < tempo_inicio:
            tempo_atual += timedelta(days=1)  # Ajuste para jogadores que passaram da meia-noite

        waiting_time = tempo_atual - tempo_inicio
        return waiting_time.total_seconds() / 60  # Retorna o tempo em minutos
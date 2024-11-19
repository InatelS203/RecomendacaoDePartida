from recomendacao.models import player

# Função para ajustar a diferença de mmr, considerando o tempo de espera
def ajustar_dif_mmr(jogador):
    return 100 + (jogador.tempoEspera() * 5)

# Função para ajustar a diferença de toxicidade, considerando o tempo de espera
def ajustar_dif_toxicidade(jogador):
    return 1.0 + (jogador.tempoEspera() * 0.1)

# Função para verificar se os jogadores estão na mesma região
def mesma_regiao(jogador, outro_jogador):
    if jogador.tempoEspera() < 10:
        return jogador.localizacao == outro_jogador.localizacao
    return True  # Ignora a localização após 10 minutos

def ajustar_dif_recompensa(jogador, outro_jogador):
    dif_recompensa = abs(jogador.mmr - outro_jogador.mmr) / 10
    if jogador.mmr < outro_jogador.mmr:
        jogador.recompensa = max(jogador.recompensa - dif_recompensa, 0)  # Evitar valores negativos
        outro_jogador.recompensa = min(outro_jogador.recompensa + dif_recompensa, 100)  # Limitar max
    else:
        jogador.recompensa = min(jogador.recompensa + dif_recompensa, 100)
        outro_jogador.recompensa = max(outro_jogador.recompensa - dif_recompensa, 0)


def match_players(players):
    prontos = []
    procurando = list(players)

    while procurando:

        atual_jogador = procurando.pop(0)
        oponente = None

        dif_mmr = ajustar_dif_mmr(atual_jogador)
        dif_toxicidade = ajustar_dif_toxicidade(atual_jogador)

        for other_player in procurando:
            if (
                abs(atual_jogador.mmr - other_player.mmr) <= dif_mmr and
                abs(atual_jogador.toxicidade - other_player.toxicidade) <= dif_toxicidade and
                mesma_regiao(atual_jogador, other_player)
            ):
                
                # Found a suitable match
                oponente = other_player
                ajustar_dif_recompensa(atual_jogador, oponente)
                break
        
        if oponente:
            prontos.append((atual_jogador, oponente))
            procurando.remove(oponente)
        else:
            procurando.append(atual_jogador)  # Requeue procurando player for next iteration
    
    return prontos

def matchmaking():
    waiting_players = player.objects.all()

    if not waiting_players:
        print("sem jogadores procurando partida")
        return []

    # Sort by queue time (longest waiting players first)
    waiting_players = sorted(
        waiting_players,
        key=lambda p: p.tempoEspera(),
        reverse=True,
    )

    return match_players(waiting_players)



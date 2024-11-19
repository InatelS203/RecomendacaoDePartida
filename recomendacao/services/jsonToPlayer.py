from django.utils.dateparse import parse_time
from django.db import transaction
from recomendacao.models import player, Rank


def processar_json(data):
    """
    Processa o JSON contendo todos os jogadores, atualiza o banco de dados
    e remove jogadores que não estão no JSON.

    Args:
        data (list): Lista de jogadores no formato JSON.
    """
    # Criar um conjunto de IDs do JSON para facilitar as comparações
    json_player_ids = set(item["id"] for item in data)

    # Abrir uma transação para garantir consistência no banco de dados
    with transaction.atomic():
        for item in data:
            # Obter a faixa de rank do jogador
            faixa_rank = obter_faixa_rank(item["rank"])
            
            # Use `get_or_create` para evitar duplicatas
            player_obj, created = player.objects.get_or_create(
                id=item["id"],  # Checagem de duplicatas por ID
                defaults={
                    "nome": item["nome"],
                    "rank": faixa_rank,  # Atribui a faixa de rank
                    "toxicidade": item["toxicidade"],
                    "localizacao": item["localizacao"],
                    "tempoProcura": parse_time(item["tempoProcura"]),
                },
            )
            if created:
                print(f"Player {player_obj.nome} created with rank {faixa_rank}.")
            else:
                print(f"Player {player_obj.nome} already exists.")
        
        # Obter todos os jogadores existentes no banco
        players_in_db = player.objects.all()

        # Deletar jogadores que não estão no JSON
        players_to_delete = players_in_db.exclude(id__in=json_player_ids)
        
        for p in players_to_delete:
            p.delete()
            print(f"Player {p.nome} deleted.")


def obter_faixa_rank(rank_value):
    """
    Encontra a faixa de rank com base no valor do rank.

    Args:
        rank_value (int): Valor do rank do jogador.

    Returns:
        Rank: Objeto da faixa de rank correspondente.
    """
    try:
        return Rank.objects.get(
            intervalo_minimo__lte=rank_value,
            intervalo_maximo__gte=rank_value
        )
    except Rank.DoesNotExist:
        return None

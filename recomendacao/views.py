from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import player
from .services.matchmaking import matchmaking
from .services import jsonToPlayer

@csrf_exempt
def matchmaking_api(request):
    if request.method == 'POST':
        try:
            # Carregar o JSON do corpo da requisição
            json_data = json.loads(request.body.decode('utf-8'))

            # Atualizar os jogadores no banco de dados com base no JSON
            jsonToPlayer(json_data)  # Função que você já criou para processar o JSON

            # Obter todos os jogadores que estão esperando por uma partida
            jogadores = player.objects.all()

            if jogadores.exists():
                # Chamar o matchmaking
                matches = matchmaking(jogadores)
                if matches:
                    return JsonResponse({
                        "matches": [
                            {"player_1": match[0].nome, "player_2": match[1].nome}
                            for match in matches
                        ]
                    }, status=200)
                else:
                    return JsonResponse({"message": "Sem partidas disponíveis no momento."}, status=200)
            else:
                return JsonResponse({"message": "Não há jogadores esperando no momento."}, status=200)
        except json.JSONDecodeError:
                    return JsonResponse({"error": "JSON inválido."}, status=400)
        except Exception as e:
                    return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Método não permitido. Use POST."}, status=405)
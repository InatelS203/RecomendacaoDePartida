🎮 Matchmaking API

Bem-vindo ao Matchmaking API, um projeto que implementa um sistema de matchmaking para jogadores baseado em critérios como MMR, toxicidade e localização. Este sistema utiliza Django para gerenciar os dados e expor uma API para integração.

Este sistema é responsável por:

Receber um JSON com informações de todos os jogadores disponíveis.
Atualizar o banco de dados com os jogadores recebidos.
Realizar o processo de matchmaking com base nos critérios configurados.
Retornar os pares de jogadores que podem formar partidas.

🛠️ Funcionalidades

Processamento de JSON: Integra dados externos de jogadores e sincroniza com o banco de dados.
Matchmaking Dinâmico: Gera partidas entre jogadores considerando:
Diferença de MMR ajustada pelo tempo de espera.
Compatibilidade de toxicidade.
Localização (opcional dependendo do tempo de espera).
API JSON: Endpoints para interação com o sistema.

⚙️ Tecnologias Utilizadas

Backend: Django
Banco de Dados: SQLite (configuração padrão, pode ser substituído por outro banco como MySQL ou PostgreSQL)
Linguagem: Python 3.8+
Bibliotecas Adicionais:
django-utils-timezone: Manipulação de tempo.
json: Processamento de dados JSON.

🚀 Como Rodar o Projeto

Pré-requisitos
Python 3.8+
pip (gerenciador de pacotes do Python)
Virtualenv (opcional, mas recomendado)
Passos
Clone o repositório:
git clone https://github.com/seu-usuario/matchmaking-api.git
cd matchmaking-api
Crie um ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
Instale as dependências:
pip install -r requirements.txt
Aplique as migrações:
python manage.py makemigrations
python manage.py migrate
Inicie o servidor:
python manage.py runserver
Teste a API: Acesse http://127.0.0.1:8000/api/matchmaking/ com uma ferramenta como Postman ou curl.


🔍 API Endpoints

POST /api/matchmaking/
Descrição: Recebe um JSON com dados de jogadores, atualiza o banco e retorna pares formados.
Body (exemplo):
[
    {
        "id": 1,
        "nome": "Player1",
        "rank": 1200,
        "toxicidade": 8.5,
        "localizacao": "Região A",
        "tempoProcura": "12:00:00"
    },
    {
        "id": 2,
        "nome": "Player2",
        "rank": 1150,
        "toxicidade": 7.0,
        "localizacao": "Região B",
        "tempoProcura": "12:01:00"
    }
]
Resposta (exemplo):
{
    "matches": [
        {
            "player_1": "Player1",
            "player_2": "Player2"
        }
    ]
}
Erros Comuns:
400 JSON inválido.: O corpo da requisição não está no formato esperado.
500 Erro Interno.: Falha ao processar o matchmaking.
📈 Melhorias Futuras

Persistência de Logs: Salvar histórico de partidas.
Fila Dinâmica: Processar requisições em tempo real com WebSocket.
Configuração Personalizada: Permitir ajustar critérios de matchmaking por jogador.
Autenticação: Adicionar autenticação para segurança das rotas.
Feito com ❤️ e Python! 🐍
Se encontrar problemas ou tiver sugestões, sinta-se à vontade para abrir um issue ou enviar um pull request. 😊

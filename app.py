from flask import Flask, jsonify
import random

app = Flask(__name__)

# Configurações gerais do jogo
NUM_PLAYERS = 4  # Número de jogadores
INITIAL_BALANCE = 300  # Saldo inicial de cada jogador
NUM_PROPERTIES = 20  # Número de propriedades no tabuleiro
BOARD_LAP_BONUS = 100  # Bônus ao completar uma volta no tabuleiro
MAX_ROUNDS = 1000  # Limite de rodadas para o término do jogo

# Criação das propriedades com valores de custo e aluguel variáveis
properties = [{'cost': random.randint(50, 150), 'rent': random.randint(10, 100), 'owner': None} for _ in range(NUM_PROPERTIES)]

# Classe que representa cada jogador e seu comportamento no jogo
class Player:
    def __init__(self, name, behavior):
        self.name = name  # Nome do jogador, baseado no tipo de comportamento
        self.balance = INITIAL_BALANCE  # Saldo inicial definido para o jogador
        self.position = 0  # Posição inicial no tabuleiro
        self.owned_properties = []  # Lista de propriedades possuídas
        self.behavior = behavior  # Comportamento do jogador

    # Movimentação do jogador no tabuleiro (dado de 6 faces)
    def move(self):
        steps = random.randint(1, 6)  # Jogada de dado para determinar o número de passos
        self.position = (self.position + steps) % NUM_PROPERTIES  # Atualiza posição no tabuleiro
        return self.position

    # Lógica de decisão de compra conforme o comportamento do jogador
    def decide_purchase(self, property):
        if property['owner'] is not None:
            return False  # Propriedade já tem dono
        cost = property['cost']
        # Condições de compra baseadas no comportamento
        if self.behavior == "impulsivo":
            return self.balance >= cost
        elif self.behavior == "exigente":
            return self.balance >= cost and property['rent'] > 50
        elif self.behavior == "cauteloso":
            return self.balance >= cost + 80
        elif self.behavior == "aleatorio":
            return self.balance >= cost and random.choice([True, False])
        return False

    # Métodos de pagamento e recebimento, ajustando o saldo do jogador
    def pay(self, amount):
        self.balance -= amount

    def receive(self, amount):
        self.balance += amount

# Inicialização dos jogadores com comportamentos específicos
players = [
    Player("impulsivo", "impulsivo"),
    Player("exigente", "exigente"),
    Player("cauteloso", "cauteloso"),
    Player("aleatorio", "aleatorio")
]

# Função para resetar o estado do jogo, útil para reiniciar a simulação
def reset_game():
    global players, properties
    properties = [{'cost': random.randint(50, 150), 'rent': random.randint(10, 100), 'owner': None} for _ in range(NUM_PROPERTIES)]
    players = [
        Player("impulsivo", "impulsivo"),
        Player("exigente", "exigente"),
        Player("cauteloso", "cauteloso"),
        Player("aleatorio", "aleatorio")
    ]

# Função principal que simula o jogo, rodando até que uma condição de fim seja alcançada
def simulate_game():
    reset_game()  # Reinicia o jogo antes de cada simulação
    for round in range(MAX_ROUNDS):  # Limita a simulação ao número máximo de rodadas
        for player in players:
            if player.balance < 0:  # Verifica se o jogador está eliminado
                continue

            position = player.move()  # Move o jogador no tabuleiro
            property = properties[position]  # Propriedade na posição atual

            # Caso a propriedade já tenha dono e não seja o próprio jogador
            if property['owner'] is not None and property['owner'] != player:
                owner = property['owner']
                rent = property['rent']
                player.pay(rent)  # Paga o aluguel ao proprietário
                owner.receive(rent)  # Proprietário recebe o aluguel
                if player.balance < 0:
                    player.owned_properties = []  # Remove propriedades caso saldo fique negativo
            else:
                # Decisão de compra caso a propriedade não tenha dono
                if player.decide_purchase(property):
                    player.pay(property['cost'])  # Paga pelo custo da propriedade
                    property['owner'] = player  # Define o jogador como proprietário
                    player.owned_properties.append(property)

            # Bônus por completar uma volta no tabuleiro
            if position < player.position:
                player.receive(BOARD_LAP_BONUS)

        # Checa se há apenas um jogador com saldo positivo, declarando-o vencedor
        active_players = [p for p in players if p.balance > 0]
        if len(active_players) == 1:
            return active_players[0]

    # Caso o limite de rodadas seja atingido, o vencedor é o com maior saldo
    active_players.sort(key=lambda p: p.balance, reverse=True)
    return active_players[0]

# Rota de simulação do jogo, que retorna o vencedor e a lista de jogadores ordenados por saldo
@app.route('/jogo/simular', methods=['GET'])
def simulate():
    winner = simulate_game()
    sorted_players = sorted(players, key=lambda p: p.balance, reverse=True)
    return jsonify({
        'vencedor': winner.name,
        'jogadores': [p.name for p in sorted_players]
    })

if __name__ == '__main__':
    app.run(port=8080)

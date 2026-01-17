# Introdução ao Método de Hondt (para o sistema de eleição proporcional português):
# - Cada partido político apresenta uma lista de candidatos.
# - Os eleitores votam na lista de um partido.
# - Os votos são contados e os assentos são distribuídos proporcionalmente com base no número de votos recebidos por cada partido.
# - O método de Hondt utiliza uma série de divisores para calcular a distribuição dos assentos.
# - O partido com o maior quociente recebe o próximo assento, e o processo é repetido até que todos os assentos sejam distribuídos.
# - Este método tende a favorecer partidos maiores, mas também permite representação para partidos menores.
# - O objetivo é garantir uma representação proporcional no parlamento com base nos votos recebidos.

# Define os votos iniciais de cada partido
def definirVotosPorPartido(partido: str, votos: int) -> dict:
    return {"partido": partido, "votos": votos, "seats": 0}

# Define os partidos participantes
def definirPartidos(partidos: list) -> list:
    partidos_list = []

    for partido in partidos:
        partidos_list.append(partido)

    return partidos_list

# Calcula o quociente para um partido com base nos votos e no número de assentos já atribuídos
def calcularQuociente(votos: int, divisores: int) -> float:
    return votos / divisores

# Distribui os assentos entre os partidos com base no método de Hondt
def distribuirAssentos(partidos: list, total_assentos: int) -> list:
    for _ in range(total_assentos):
        quocientes = []
        for partido in partidos:
            quociente = calcularQuociente(partido["votos"], partido["seats"] + 1)
            quocientes.append((quociente, partido))

        # Encontrar o partido com o maior quociente
        maior_quociente, partido_vencedor = max(quocientes, key=lambda x: x[0])
        partido_vencedor["seats"] += 1

    return partidos

# Sistema dinâmico para entrada de dados pelo usuário
def main():
    partidos_input = int(input("Digite o número de partidos: "))
    partidos = []

    for _ in range(partidos_input):
        nome_partido = input("Digite o nome do partido: ")
        votos_partido = int(input(f"Digite o número de votos para o partido {nome_partido}: "))
        partido = definirVotosPorPartido(nome_partido, votos_partido)
        partidos.append(partido)

    total_assentos = int(input("Digite o número total de assentos a distribuir: "))

    resultados = distribuirAssentos(partidos, total_assentos)

    print("\nDistribuição final dos assentos:")
    for partido in resultados:
        print(f"Partido: {partido['partido']}, Assentos: {partido['seats']}")

if __name__ == "__main__":
    main()
import json
from typing import List, Dict

from main import definirVotosPorPartido, distribuirAssentos


def seats_distribution(partidos: List[Dict], total_assentos: int) -> Dict[str, int]:
    resultados = distribuirAssentos(partidos, total_assentos)
    return {p["partido"]: p["seats"] for p in resultados}


def test_basic_two_parties():
    # 1000 vs 500 votos, 5 assentos => A recebe 4, B recebe 1 (D'Hondt)
    A = definirVotosPorPartido("A", 1000)
    B = definirVotosPorPartido("B", 500)
    dist = seats_distribution([A, B], 5)
    assert dist["A"] == 4
    assert dist["B"] == 1


def test_three_parties_example():
    # Exemplo simples
    A = definirVotosPorPartido("A", 340000)
    B = definirVotosPorPartido("B", 280000)
    C = definirVotosPorPartido("C", 160000)
    D = definirVotosPorPartido("D", 60000)
    dist = seats_distribution([A, B, C, D], 7)
    assert dist["A"] == 3
    assert dist["B"] == 3
    assert dist["C"] == 1
    assert dist["D"] == 0


def test_tie_strategy_alpha():
    # Empate deliberado: mesmos votos, 1 assento, alpha deve escolher pelo nome
    X = definirVotosPorPartido("Beta", 1000)
    Y = definirVotosPorPartido("Alpha", 1000)
    resultados = distribuirAssentos([X, Y], 1, tie_strategy="alpha")
    # Alpha (por ordem alfabética) deve vencer
    seats = {p["partido"]: p["seats"] for p in resultados}
    assert seats["Alpha"] == 1
    assert seats["Beta"] == 0

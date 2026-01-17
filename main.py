import argparse
import csv
import json
import os
import random
from typing import List, Dict, Tuple, Optional

# Introdução ao Método de Hondt (para o sistema de eleição proporcional português):
# - Cada partido político apresenta uma lista de candidatos.
# - Os eleitores votam na lista de um partido.
# - Os votos são contados e os assentos são distribuídos proporcionalmente com base no número de votos recebidos por cada partido.
# - O método de Hondt utiliza uma série de divisores para calcular a distribuição dos assentos.
# - O partido com o maior quociente recebe o próximo assento, e o processo é repetido até que todos os assentos sejam distribuídos.
# - Este método tende a favorecer partidos maiores, mas também permite representação para partidos menores.
# - O objetivo é garantir uma representação proporcional no parlamento com base nos votos recebidos.

# Define os votos iniciais de cada partido
def definirVotosPorPartido(partido: str, votos: int) -> Dict:
    return {"partido": partido, "votos": int(votos), "seats": 0}

# Define os partidos participantes
def definirPartidos(partidos: List[Dict]) -> List[Dict]:
    return list(partidos)

# Calcula o quociente para um partido com base nos votos e no número de assentos já atribuídos
def calcularQuociente(votos: int, divisores: int) -> float:
    return votos / divisores

# Distribui os assentos entre os partidos com base no método de Hondt
def distribuirAssentos(
    partidos: List[Dict],
    total_assentos: int,
    tie_strategy: str = "votes_alpha",
    show_table: bool = False,
    table_log: Optional[List[Dict]] = None,
) -> List[Dict]:
    """Distribui assentos segundo D'Hondt com estratégia de desempate configurável.

    tie_strategy opções:
      - "votes": maior número de votos totais
      - "alpha": ordem alfabética do nome
      - "input": ordem de entrada (primeiro definido vence)
      - "random": escolha aleatória
      - "votes_alpha": votos desc, depois nome asc (default)
    """

    if total_assentos <= 0:
        raise ValueError("total_assentos deve ser > 0")

    if not partidos:
        raise ValueError("Lista de partidos vazia")

    # Preservar ordem de entrada
    indice_por_partido = {p["partido"]: i for i, p in enumerate(partidos)}

    for ronda in range(1, total_assentos + 1):
        quocientes: List[Tuple[float, Dict]] = []
        for partido in partidos:
            quociente = calcularQuociente(partido["votos"], partido["seats"] + 1)
            quocientes.append((quociente, partido))

        # Maior quociente
        maior_quociente = max(q for q, _ in quocientes)
        candidatos = [(q, p) for q, p in quocientes if q == maior_quociente]

        def escolher_vencedor(cands: List[Tuple[float, Dict]]) -> Dict:
            if len(cands) == 1:
                return cands[0][1]

            if tie_strategy == "votes":
                return max((p for _, p in cands), key=lambda p: p["votos"])
            elif tie_strategy == "alpha":
                return min((p for _, p in cands), key=lambda p: p["partido"].lower())
            elif tie_strategy == "input":
                return min((p for _, p in cands), key=lambda p: indice_por_partido[p["partido"]])
            elif tie_strategy == "random":
                return random.choice([p for _, p in cands])
            else:  # votes_alpha
                # Primeiro por votos desc, depois nome asc
                return sorted((p for _, p in cands), key=lambda p: (-p["votos"], p["partido"].lower()))[0]

        partido_vencedor = escolher_vencedor(candidatos)
        partido_vencedor["seats"] += 1

        if show_table:
            print(
                f"Ronda {ronda}: vencedor {partido_vencedor['partido']} (quociente {maior_quociente:.2f})"
            )

        if table_log is not None:
            table_log.append(
                {
                    "ronda": ronda,
                    "vencedor": partido_vencedor["partido"],
                    "quociente_vencedor": round(maior_quociente, 6),
                    "quocientes": [
                        {
                            "partido": p["partido"],
                            "quociente": round(q, 6),
                            "seats_antes": p["seats"],
                        }
                        for q, p in quocientes
                    ],
                }
            )

    return partidos


def validar_partidos(partidos: List[Dict]) -> None:
    for p in partidos:
        if not isinstance(p.get("partido"), str) or not p["partido"].strip():
            raise ValueError("Nome de partido inválido")
        if int(p.get("votos", -1)) < 0:
            raise ValueError(f"Votos inválidos para partido {p.get('partido')}")


def ordenar_resultados(partidos: List[Dict], sort_by: str = "seats", desc: bool = True) -> List[Dict]:
    chave = (
        (lambda p: p["seats"]) if sort_by == "seats" else (
            (lambda p: p["votos"]) if sort_by == "votos" else (lambda p: p["partido"].lower())
        )
    )
    return sorted(partidos, key=chave, reverse=desc)


def imprimir_resultados(partidos: List[Dict]) -> None:
    total_votos = sum(p["votos"] for p in partidos)
    print("\nDistribuição final dos assentos:")
    for p in partidos:
        percent = (p["votos"] / total_votos * 100) if total_votos > 0 else 0.0
        print(
            f"Partido: {p['partido']}, Votos: {p['votos']} ({percent:.2f}%), Assentos: {p['seats']}"
        )


def exportar_csv(caminho: str, partidos: List[Dict], table_log: Optional[List[Dict]] = None) -> None:
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["partido", "votos", "assentos"])
        for p in partidos:
            writer.writerow([p["partido"], p["votos"], p["seats"]])
    # Tabela de rondas (se fornecida) em arquivo separado
    if table_log is not None:
        base, ext = os.path.splitext(caminho)
        tabela_path = f"{base}.rondas{ext or '.csv'}"
        with open(tabela_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ronda", "vencedor", "quociente_vencedor", "partido", "quociente", "seats_antes"])
            for row in table_log:
                for q in row["quocientes"]:
                    writer.writerow([
                        row["ronda"], row["vencedor"], row["quociente_vencedor"], q["partido"], q["quociente"], q["seats_antes"],
                    ])


def exportar_json(caminho: str, partidos: List[Dict], table_log: Optional[List[Dict]] = None) -> None:
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    payload = {"resultados": partidos}
    if table_log is not None:
        payload["rondas"] = table_log
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def gerar_grafico(partidos: List[Dict], caminho: str) -> None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        print("Aviso: matplotlib não está disponível. Instale via 'pip install matplotlib'.")
        return
    os.makedirs(os.path.dirname(caminho) or ".", exist_ok=True)
    nomes = [p["partido"] for p in partidos]
    seats = [p["seats"] for p in partidos]
    votos = [p["votos"] for p in partidos]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = range(len(nomes))
    ax.bar(x, seats, label="Assentos", color="#4e79a7")
    ax.set_xticks(list(x))
    ax.set_xticklabels(nomes, rotation=30, ha="right")
    ax.set_ylabel("Assentos")
    ax.set_title("Distribuição de Assentos (Método de Hondt)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close(fig)


def ler_csv(caminho: str) -> List[Dict]:
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"CSV não encontrado: {caminho}")
    partidos: List[Dict] = []
    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Aceita colunas: partido,nome e votos
        for row in reader:
            nome = row.get("partido") or row.get("nome") or row.get("name")
            votos = row.get("votos") or row.get("votes")
            if nome is None or votos is None:
                raise ValueError("CSV deve conter colunas 'partido'/'nome' e 'votos'/'votes'")
            partidos.append(definirVotosPorPartido(str(nome).strip(), int(votos)))
    return partidos


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Simulador do Método de Hondt (Português)",
    )
    parser.add_argument("--csv", dest="csv", help="Caminho para CSV com colunas partido,votos")
    parser.add_argument("--seats", dest="seats", type=int, help="Número total de assentos a distribuir")
    parser.add_argument(
        "--tie",
        dest="tie",
        default="votes_alpha",
        choices=["votes", "alpha", "input", "random", "votes_alpha"],
        help="Estratégia de desempate (default: votes_alpha)",
    )
    parser.add_argument("--show-table", dest="show_table", action="store_true", help="Mostrar rondas/vencedores")
    parser.add_argument("--out-csv", dest="out_csv", help="Exportar resultados para CSV (e rondas para .rondas.csv)")
    parser.add_argument("--out-json", dest="out_json", help="Exportar resultados/tabela para JSON")
    parser.add_argument("--graph", dest="graph", help="Salvar gráfico de assentos (ex.: outputs/assentos.png)")
    parser.add_argument(
        "--sort-by",
        dest="sort_by",
        default="seats",
        choices=["seats", "votos", "nome"],
        help="Ordenação da saída (default: seats)",
    )
    parser.add_argument(
        "--asc",
        dest="asc",
        action="store_true",
        help="Ordenar em ascendente (por defeito: descendente)",
    )
    return parser.parse_args()

# Sistema dinâmico para entrada de dados pelo usuário
def main():
    args = parse_args()

    if args.csv and args.seats:
        partidos = ler_csv(args.csv)
        validar_partidos(partidos)
        table_log: List[Dict] = [] if (args.out_csv or args.out_json) else None
        resultados = distribuirAssentos(partidos, args.seats, tie_strategy=args.tie, show_table=args.show_table, table_log=table_log)
        sort_key = "seats" if args.sort_by == "seats" else ("votos" if args.sort_by == "votos" else "nome")
        # Adaptar chave 'nome' para 'partido'
        if sort_key == "nome":
            resultados = sorted(resultados, key=lambda p: p["partido"].lower(), reverse=not args.asc)
        else:
            resultados = ordenar_resultados(resultados, sort_by=sort_key, desc=not args.asc)
        imprimir_resultados(resultados)
        if args.out_csv:
            exportar_csv(args.out_csv, resultados, table_log)
            print(f"Resultados CSV salvos em: {args.out_csv}")
        if args.out_json:
            exportar_json(args.out_json, resultados, table_log)
            print(f"Resultados JSON salvos em: {args.out_json}")
        if args.graph:
            gerar_grafico(resultados, args.graph)
            print(f"Gráfico salvo em: {args.graph}")
        return

    # Fallback interativo
    print("Modo interativo (use --csv e --seats para modo automático)\n")
    partidos_input = int(input("Digite o número de partidos: "))
    partidos: List[Dict] = []
    for _ in range(partidos_input):
        nome_partido = input("Digite o nome do partido: ").strip()
        votos_partido = int(input(f"Digite o número de votos para o partido {nome_partido}: "))
        partidos.append(definirVotosPorPartido(nome_partido, votos_partido))

    total_assentos = int(input("Digite o número total de assentos a distribuir: "))
    validar_partidos(partidos)
    table_log: Optional[List[Dict]] = None
    resultados = distribuirAssentos(partidos, total_assentos, tie_strategy=args.tie, show_table=args.show_table, table_log=table_log)
    resultados = ordenar_resultados(resultados, sort_by="seats", desc=True)
    imprimir_resultados(resultados)

if __name__ == "__main__":
    main()
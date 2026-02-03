import numpy as np
import pandas as pd
from collections import Counter
from dataclasses import dataclass, replace
from typing import List, Dict, Tuple, Set


# =========================
# Dataclasses (inmutables)
# =========================

@dataclass(frozen=True)
class SimParams:
    P_values: List[int]
    R_values: List[int]
    n_matches: int
    alpha: float = 0.0   # si luego querés sesgo al último, lo usás


@dataclass(frozen=True)
class VoteContext:
    P: int
    R: int
    match_id: int
    round_id: int
    step_id: int          # step de votación (cada step elimina a alguien)
    impostors: Set[int]


def update_ctx(ctx: VoteContext, **changes) -> VoteContext:
    return replace(ctx, **changes)


# =========================
# Helpers puros
# =========================

def choose_targets(players_alive: List[int], rng: np.random.Generator) -> List[int]:
    """
    Devuelve la lista de targets votados en ESTE step (uno por voter).
    El orden coincide con players_alive (voter recorre players_alive).
    """
    targets = []
    for voter in players_alive:
        possible_targets = [p for p in players_alive if p != voter]
        target = rng.choice(possible_targets)
        targets.append(target)
    return targets


def pick_eliminated_from_targets(targets: List[int], rng: np.random.Generator) -> Tuple[int, int, List[int]]:
    """
    targets: lista de targets (uno por voto).
    Retorna:
      - eliminated (int)
      - max_votes (int)
      - most_voted (lista de empatados)
    """
    count_votes = Counter(targets)
    max_votes = max(count_votes.values())
    most_voted = [player for player, v in count_votes.items() if v == max_votes]
    eliminated = rng.choice(most_voted)
    return eliminated, max_votes, most_voted


def impostors_win(players_alive: List[int], impostors: Set[int]) -> bool:
    """
    Condición: impostores ganan si #impostores >= #civiles.
    (Es lo típico: paridad o ventaja)
    """
    alive_set = set(players_alive)
    n_imp = len(alive_set & impostors)
    n_civ = len(alive_set - impostors)
    return n_imp >= n_civ


def append_votes_rows(
    votes: List[Dict],
    ctx: VoteContext,
    players_alive: List[int],
    targets: List[int],
):
    """
    Agrega 1 fila por voto (voter -> target).
    """
    for voter, target in zip(players_alive, targets):
        votes.append({
            "P": ctx.P,
            "R": ctx.R,
            "match": ctx.match_id,
            "round": ctx.round_id,
            "step": ctx.step_id,
            "voter": voter,
            "target": target,
            "voter_role": "impostor" if voter in ctx.impostors else "civil",
            "target_role": "impostor" if target in ctx.impostors else "civil",
        })


def append_game_result_row(
    game_results: List[Dict],
    ctx: VoteContext,
    eliminated: int,
    max_votes: int,
    tie_size: int,
    impostors_wins_flag: bool,
):
    """
    Agrega 1 fila por step (una eliminación).
    """
    game_results.append({
        "P": ctx.P,
        "R": ctx.R,
        "match": ctx.match_id,
        "round": ctx.round_id,
        "step": ctx.step_id,
        "eliminated": eliminated,
        "eliminated_role": "impostor" if eliminated in ctx.impostors else "civil",
        "max_votes": max_votes,
        "tie_size": tie_size,
        "impostors_wins": impostors_wins_flag,
    })


# =========================
# Core simulation
# =========================

def simulate_round(
    base_ctx: VoteContext,
    players: List[int],
    rng: np.random.Generator,
    votes: List[Dict],
    game_results: List[Dict],
) -> None:
    """
    Simula una ronda completa hasta que:
      - se elimina el impostor, o
      - el impostor gana por paridad.
    Guarda filas en votes y game_results.
    """

    players_alive = players.copy()
    step_id = 0

    # mientras el impostor siga vivo y no haya ganado por paridad
    while (len(set(players_alive) & base_ctx.impostors) > 0) and (not impostors_win(players_alive, base_ctx.impostors)):
        step_id += 1
        ctx = update_ctx(base_ctx, step_id=step_id)

        targets = choose_targets(players_alive, rng)
        append_votes_rows(votes, ctx, players_alive, targets)

        eliminated, max_votes, most_voted = pick_eliminated_from_targets(targets, rng)
        players_alive.remove(eliminated)

        imp_win_flag = impostors_win(players_alive, ctx.impostors)
        append_game_result_row(
            game_results,
            ctx,
            eliminated=eliminated,
            max_votes=max_votes,
            tie_size=len(most_voted),
            impostors_wins_flag=imp_win_flag
        )

    # Si salimos porque el impostor ya no está vivo, impostors_wins queda False en el último row.
    # Si salimos por paridad, en el último row ya quedó True.


def simulate_match(
    P: int,
    R: int,
    match_id: int,
    rng: np.random.Generator,
    votes: List[Dict],
    game_results: List[Dict],
) -> None:
    """
    Simula un match con R rondas. Cada ronda:
      - resetea jugadores vivos
      - elige nuevo impostor
      - corre simulate_round
    """
    players = list(range(P))

    for round_id in range(1, R + 1):
        impostor = rng.choice(players)
        impostors = {int(impostor)}

        base_ctx = VoteContext(
            P=P,
            R=R,
            match_id=match_id,
            round_id=round_id,
            step_id=0,
            impostors=impostors,
        )

        simulate_round(base_ctx, players, rng, votes, game_results)


def run_complete_simulation(params: SimParams, seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(seed)

    votes: List[Dict] = []
    game_results: List[Dict] = []

    match_id = 0

    for P in params.P_values:
        for R in params.R_values:
            for _ in range(params.n_matches):
                match_id += 1
                simulate_match(P=P, R=R, match_id=match_id, rng=rng, votes=votes, game_results=game_results)

    votes_df = pd.DataFrame(votes)
    results_df = pd.DataFrame(game_results)
    return votes_df, results_df

        




                    
                

            
        
        
        


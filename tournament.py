from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    InvalidStrategyError,
    NormalStrategy,
)

Opponent = tuple[CreatureFactory, BattleStrategy]


def opponent_label(opponent: Opponent) -> str:
    factory, strategy = opponent
    creature_name = factory.create_base().name
    strategy_name = type(strategy).__name__.replace("Strategy", "")
    return f"({creature_name}+{strategy_name})"


def battle(opponents: list[Opponent]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    try:
        for i in range(len(opponents)):
            for j in range(i + 1, len(opponents)):
                factory_a, strategy_a = opponents[i]
                factory_b, strategy_b = opponents[j]
                fighter_a = factory_a.create_base()
                fighter_b = factory_b.create_base()
                print("\n* Battle *")
                print(fighter_a.describe())
                print(" vs.")
                print(fighter_b.describe())
                print(" now fight!")
                for line in strategy_a.act(fighter_a):
                    print(line)
                for line in strategy_b.act(fighter_b):
                    print(line)
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def run(title: str, opponents: list[Opponent]) -> None:
    print(title)
    labels = ", ".join(opponent_label(opp) for opp in opponents)
    print(f" [ {labels} ]")
    battle(opponents)


if __name__ == "__main__":
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    basic: list[Opponent] = [(flame, normal), (transform, aggressive)]
    broken: list[Opponent] = [(transform, aggressive), (flame, aggressive)]

    run("Tournament 0 (basic)", basic)
    print()
    run("Tournament 1 (error)", broken)
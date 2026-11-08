from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    fighter_a = first.create_base()
    fighter_b = second.create_base()
    print(fighter_a.describe())
    print(" vs.")
    print(fighter_b.describe())
    print(" fight!")
    print(fighter_a.attack())
    print(fighter_b.attack())


if __name__ == "__main__":
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    test_factory(flame)
    print()
    test_factory(transform)
    print()
    test_battle(flame, transform)
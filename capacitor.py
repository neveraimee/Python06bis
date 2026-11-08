from ex3 import TransformCreatureFactory
from ex3.capability import TransformCapability
from ex3.creature import Creature


def test_creature(label: str, creature: Creature) -> None:
    print(f" {label}:")
    print(creature.describe())
    print(creature.attack())
    if not isinstance(creature, TransformCapability):
        print(f"{creature.name} cannot transform")
        return
    print(creature.transform())
    print(creature.attack())
    print(creature.revert())


if __name__ == "__main__":
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    test_creature("base", factory.create_base())
    test_creature("evolved", factory.create_evolved())
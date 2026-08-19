from dataclasses import dataclass
from core.stats import Stats


@dataclass(frozen=True)
class Boss:
    name: str
    title: str
    stats: Stats
    exp_reward: int
    floor: int
    intro_text: str
    sprite: str = ""
    gold_reward: int = 0

    def is_alive(self) -> bool:
        return self.stats.is_alive()

    def take_damage(self, amount: int) -> "Boss":
        return Boss(
            name=self.name, title=self.title,
            stats=self.stats.take_damage(amount),
            exp_reward=self.exp_reward, floor=self.floor,
            intro_text=self.intro_text, sprite=self.sprite,
            gold_reward=self.gold_reward,
        )

    def __str__(self) -> str:
        return f"[BOSS] {self.name}, {self.title} [{self.stats}]"


GUARDIAN = Boss(
    name="Guardiao do 1o Circulo",
    title="Sentinela de Pedra",
    stats=Stats.create(hp=100, atk=14, defense=8, speed=3),
    exp_reward=200, floor=5, gold_reward=80,
    sprite="boss_guardiao.png",
    intro_text=(
        "O chao treme. Uma figura colossal de pedra e sombra\n"
        "bloqueia sua passagem. Seus olhos brilham em vermelho.\n"
        "-- Ninguem sobe alem daqui. --"
    ),
)

LUCAS = Boss(
    name="Lucas",
    title="o Arquiteto",
    stats=Stats.create(hp=250, atk=20, defense=12, speed=10),
    exp_reward=9999, floor=10, gold_reward=500,
    sprite="boss_lucas.png",
    intro_text=(
        "No topo da torre, uma figura elegante vira-se lentamente.\n"
        "Seus olhos carregam o peso de mil batalhas.\n"
        "-- Entao voce chegou ate aqui. Impressionante.\n"
        "  Mas esta torre foi feita para nao ter fim. --\n"
        "Lucas sorri. A batalha final comeca."
    ),
)

BOSSES_BY_FLOOR: dict[int, Boss] = {
    5:  GUARDIAN,
    10: LUCAS,
}

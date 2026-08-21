from dataclasses import dataclass
from enum import Enum, auto


class SkillType(Enum):
    HEAVY_STRIKE = auto()
    DEFENSIVE_STANCE = auto()
    FIREBALL = auto()
    ARCANE_SHIELD = auto()
    SNEAK_ATTACK = auto()
    SHADOW_STEP = auto()
    GENERIC = auto()


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    cooldown: int
    mana_cost: int = 0
    skill_type: SkillType = SkillType.GENERIC
    sprite: str = ""

    def __str__(self) -> str:
        mana_info = f" | Mana: {self.mana_cost}" if self.mana_cost > 0 else ""
        return f"{self.name}: {self.description} (cooldown: {self.cooldown}t{mana_info})"


@dataclass(frozen=True)
class CharacterClass:
    name: str
    description: str
    base_hp: int
    base_atk: int
    base_defense: int
    base_speed: int
    base_mana: int
    skills: tuple[Skill, ...]
    sprite: str = ""

    def __str__(self) -> str:
        return f"{self.name} — {self.description}"


WARRIOR = CharacterClass(
    name="Guerreiro",
    description="Mestre do combate fisico. Resistente e poderoso.",
    base_hp=60,
    base_atk=8,
    base_defense=5,
    base_speed=5,
    base_mana=0,
    sprite="guerreiro.png",
    skills=(
        Skill(
            name="Golpe Pesado",
            description="Causa 2x ATK de dano, reduz VEL no proximo turno.",
            cooldown=3,
            mana_cost=0,
            skill_type=SkillType.HEAVY_STRIKE,
            sprite="skill_golpe_pesado.png",
        ),
        Skill(
            name="Postura Defensiva",
            description="Dobra a DEF por 1 turno. ATK zerado nesse turno.",
            cooldown=4,
            mana_cost=0,
            skill_type=SkillType.DEFENSIVE_STANCE,
            sprite="skill_postura_defensiva.png",
        ),
    ),
)

MAGE = CharacterClass(
    name="Mago",
    description="Manipula magia arcana. Fragil, mas letal a distancia.",
    base_hp=40,
    base_atk=5,
    base_defense=2,
    base_speed=7,
    base_mana=30,
    sprite="mago.png",
    skills=(
        Skill(
            name="Bola de Fogo",
            description="Dano magico que ignora a DEF do inimigo.",
            cooldown=2,
            mana_cost=10,
            skill_type=SkillType.FIREBALL,
            sprite="skill_bola_de_fogo.png",
        ),
        Skill(
            name="Escudo Arcano",
            description="Absorve completamente o proximo ataque recebido.",
            cooldown=5,
            mana_cost=15,
            skill_type=SkillType.ARCANE_SHIELD,
            sprite="skill_escudo_arcano.png",
        ),
    ),
)

ROGUE = CharacterClass(
    name="Ladino",
    description="Mestre da agilidade e dos ataques furtivos. Rapido e letal.",
    base_hp=45,
    base_atk=7,
    base_defense=3,
    base_speed=9,
    base_mana=15,
    sprite="ladino.png",
    skills=(
        Skill(
            name="Ataque Furtivo",
            description="Golpe preciso baseado em ATK + VEL, ignorando metade da DEF.",
            cooldown=3,
            mana_cost=5,
            skill_type=SkillType.SNEAK_ATTACK,
            sprite="skill_ataque_furtivo.png",
        ),
        Skill(
            name="Passo das Sombras",
            description="Esquiva do proximo ataque inimigo e recupera 5 de Mana.",
            cooldown=4,
            mana_cost=5,
            skill_type=SkillType.SHADOW_STEP,
            sprite="skill_passo_das_sombras.png",
        ),
    ),
)

ALL_CLASSES: dict[str, CharacterClass] = {
    WARRIOR.name: WARRIOR,
    MAGE.name: MAGE,
    ROGUE.name: ROGUE,
}

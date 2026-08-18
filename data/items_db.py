from core.items import Item, ItemSlot, Rarity

# ═══════════════════════════════════════════════════════
#  ARMAS
# ═══════════════════════════════════════════════════════

# -- Comum
WOODEN_SWORD = Item(
    name="Espada de Madeira", slot=ItemSlot.WEAPON, rarity=Rarity.COMMON,
    hp_bonus=0, atk_bonus=2, defense_bonus=0, speed_bonus=0,
    description="Uma lâmina tosca de madeira. Melhor que nada.",
    sprite="espada_madeira.png",
)
WOODEN_STAFF = Item(
    name="Cajado de Madeira", slot=ItemSlot.WEAPON, rarity=Rarity.COMMON,
    hp_bonus=0, atk_bonus=2, defense_bonus=0, speed_bonus=1,
    description="Galho de carvalho moldado às pressas.",
    sprite="cajado_madeira.png",
)

# -- Incomum
COPPER_SWORD = Item(
    name="Espada de Cobre", slot=ItemSlot.WEAPON, rarity=Rarity.UNCOMMON,
    hp_bonus=0, atk_bonus=4, defense_bonus=0, speed_bonus=0,
    description="Cobre macio, mas já causa dano real.",
    sprite="espada_cobre.png",
)
OAK_STAFF = Item(
    name="Cajado de Carvalho", slot=ItemSlot.WEAPON, rarity=Rarity.UNCOMMON,
    hp_bonus=0, atk_bonus=4, defense_bonus=0, speed_bonus=1,
    description="Canal arcano básico. Amplifica magias levemente.",
    sprite="cajado_carvalho.png",
)

# -- Raro
IRON_SWORD = Item(
    name="Espada de Ferro", slot=ItemSlot.WEAPON, rarity=Rarity.RARE,
    hp_bonus=0, atk_bonus=7, defense_bonus=1, speed_bonus=0,
    description="Forjada em ferro puro. Confiável e resistente.",
    sprite="espada_ferro.png",
)
ARCANE_STAFF = Item(
    name="Cajado Arcano", slot=ItemSlot.WEAPON, rarity=Rarity.RARE,
    hp_bonus=0, atk_bonus=8, defense_bonus=0, speed_bonus=2,
    description="Cristal arcano incrustado. Amplifica magias significativamente.",
    sprite="cajado_arcano.png",
)

# -- Épico
ABYSSAL_BLADE = Item(
    name="Lamina do Abismo", slot=ItemSlot.WEAPON, rarity=Rarity.EPIC,
    hp_bonus=5, atk_bonus=13, defense_bonus=0, speed_bonus=1,
    description="Forjada nas profundezas. Pulsa com energia sombria.",
    sprite="lamina_abismo.png",
)
VOID_STAFF = Item(
    name="Cajado do Vazio", slot=ItemSlot.WEAPON, rarity=Rarity.EPIC,
    hp_bonus=0, atk_bonus=14, defense_bonus=0, speed_bonus=3,
    description="Canalizador de magia pura. Queima a mente de quem o usa.",
    sprite="cajado_vazio.png",
)

# ═══════════════════════════════════════════════════════
#  ARMADURAS
# ═══════════════════════════════════════════════════════

CLOTH_ARMOR = Item(
    name="Armadura de Tecido", slot=ItemSlot.ARMOR, rarity=Rarity.COMMON,
    hp_bonus=5, atk_bonus=0, defense_bonus=1, speed_bonus=0,
    description="Camadas de tecido grosso. Proteção mínima.",
    sprite="armadura_tecido.png",
)
LEATHER_ARMOR = Item(
    name="Armadura de Couro", slot=ItemSlot.ARMOR, rarity=Rarity.UNCOMMON,
    hp_bonus=10, atk_bonus=0, defense_bonus=3, speed_bonus=0,
    description="Couro curtido. Leve e oferece proteção decente.",
    sprite="armadura_couro.png",
)
CHAIN_MAIL = Item(
    name="Cota de Malha", slot=ItemSlot.ARMOR, rarity=Rarity.RARE,
    hp_bonus=15, atk_bonus=0, defense_bonus=6, speed_bonus=-1,
    description="Aneis de ferro entrelaçados. Proteção sólida.",
    sprite="armadura_malha.png",
)
MAGE_ROBE = Item(
    name="Manto Arcano", slot=ItemSlot.ARMOR, rarity=Rarity.RARE,
    hp_bonus=5, atk_bonus=2, defense_bonus=3, speed_bonus=1,
    description="Encantado para auxiliar magistas. Leve e resistente.",
    sprite="armadura_manto.png",
)
SHADOW_PLATE = Item(
    name="Placa das Sombras", slot=ItemSlot.ARMOR, rarity=Rarity.EPIC,
    hp_bonus=25, atk_bonus=0, defense_bonus=10, speed_bonus=0,
    description="Forjada com metal das sombras. Absorve impactos sobrenaturais.",
    sprite="armadura_sombras.png",
)

# ═══════════════════════════════════════════════════════
#  CAPACETES
# ═══════════════════════════════════════════════════════

CLOTH_HOOD = Item(
    name="Capuz de Tecido", slot=ItemSlot.HELMET, rarity=Rarity.COMMON,
    hp_bonus=3, atk_bonus=0, defense_bonus=1, speed_bonus=0,
    description="Capuz simples de tecido.",
    sprite="capacete_capuz.png",
)
LEATHER_HELMET = Item(
    name="Elmo de Couro", slot=ItemSlot.HELMET, rarity=Rarity.UNCOMMON,
    hp_bonus=5, atk_bonus=0, defense_bonus=2, speed_bonus=0,
    description="Couro moldado para proteger a cabeça.",
    sprite="capacete_couro.png",
)
IRON_HELMET = Item(
    name="Elmo de Ferro", slot=ItemSlot.HELMET, rarity=Rarity.RARE,
    hp_bonus=5, atk_bonus=0, defense_bonus=4, speed_bonus=0,
    description="Ferro temperado. Protege bem a cabeça.",
    sprite="capacete_ferro.png",
)
ARCANE_HOOD = Item(
    name="Capuz Arcano", slot=ItemSlot.HELMET, rarity=Rarity.RARE,
    hp_bonus=0, atk_bonus=2, defense_bonus=2, speed_bonus=1,
    description="Melhora foco e precisão mágica.",
    sprite="capacete_arcano.png",
)
CROWN_OF_ABYSS = Item(
    name="Coroa do Abismo", slot=ItemSlot.HELMET, rarity=Rarity.EPIC,
    hp_bonus=10, atk_bonus=3, defense_bonus=5, speed_bonus=0,
    description="Coroa forjada no núcleo da torre. Irradia poder sombrio.",
    sprite="capacete_coroa.png",
)

# ═══════════════════════════════════════════════════════
#  BOTAS
# ═══════════════════════════════════════════════════════

CLOTH_BOOTS = Item(
    name="Botas de Tecido", slot=ItemSlot.BOOTS, rarity=Rarity.COMMON,
    hp_bonus=0, atk_bonus=0, defense_bonus=0, speed_bonus=1,
    description="Calçado básico de tecido.",
    sprite="botas_tecido.png",
)
LEATHER_BOOTS = Item(
    name="Botas de Couro", slot=ItemSlot.BOOTS, rarity=Rarity.UNCOMMON,
    hp_bonus=0, atk_bonus=0, defense_bonus=1, speed_bonus=3,
    description="Leves e confortáveis.",
    sprite="botas_couro.png",
)
IRON_BOOTS = Item(
    name="Botas de Ferro", slot=ItemSlot.BOOTS, rarity=Rarity.RARE,
    hp_bonus=5, atk_bonus=0, defense_bonus=3, speed_bonus=0,
    description="Pesadas mas resistentes.",
    sprite="botas_ferro.png",
)
SWIFT_BOOTS = Item(
    name="Botas da Celeridade", slot=ItemSlot.BOOTS, rarity=Rarity.RARE,
    hp_bonus=0, atk_bonus=0, defense_bonus=0, speed_bonus=6,
    description="Encantadas. Quem as usa parece voar.",
    sprite="botas_celeridade.png",
)
SHADOW_BOOTS = Item(
    name="Botas das Sombras", slot=ItemSlot.BOOTS, rarity=Rarity.EPIC,
    hp_bonus=0, atk_bonus=2, defense_bonus=2, speed_bonus=8,
    description="Silenciosas como a noite. Deixam rastro de sombra.",
    sprite="botas_sombras.png",
)

# ═══════════════════════════════════════════════════════
#  ANÉIS
# ═══════════════════════════════════════════════════════

COPPER_RING = Item(
    name="Anel de Cobre", slot=ItemSlot.RING, rarity=Rarity.COMMON,
    hp_bonus=5, atk_bonus=0, defense_bonus=0, speed_bonus=0,
    description="Anel simples que aumenta um pouco o vigor.",
    sprite="anel_cobre.png",
)
RING_VITALITY = Item(
    name="Anel da Vitalidade", slot=ItemSlot.RING, rarity=Rarity.UNCOMMON,
    hp_bonus=12, atk_bonus=0, defense_bonus=0, speed_bonus=0,
    description="Aumenta o vigor do portador.",
    sprite="anel_vitalidade.png",
)
RING_POWER = Item(
    name="Anel do Poder", slot=ItemSlot.RING, rarity=Rarity.RARE,
    hp_bonus=0, atk_bonus=4, defense_bonus=0, speed_bonus=0,
    description="Concentra força de ataque no punho.",
    sprite="anel_poder.png",
)
RING_WARDING = Item(
    name="Anel da Protecao", slot=ItemSlot.RING, rarity=Rarity.RARE,
    hp_bonus=0, atk_bonus=0, defense_bonus=4, speed_bonus=0,
    description="Cria um campo protetor sutil.",
    sprite="anel_protecao.png",
)
RING_OF_LUCAS = Item(
    name="Anel de Lucas", slot=ItemSlot.RING, rarity=Rarity.EPIC,
    hp_bonus=15, atk_bonus=5, defense_bonus=3, speed_bonus=3,
    description="Drop raro do Arquiteto. Concentra o poder da torre.",
    sprite="anel_lucas.png",
)

# ═══════════════════════════════════════════════════════
#  DROPS POR ANDAR  (raridade cresce com o andar)
# ═══════════════════════════════════════════════════════

from core.items import Item  # noqa — já importado acima, só garante

FLOOR_DROPS: dict[int, list[Item]] = {
    1:  [WOODEN_SWORD, WOODEN_STAFF, CLOTH_ARMOR, CLOTH_BOOTS, CLOTH_HOOD, COPPER_RING],
    2:  [WOODEN_SWORD, WOODEN_STAFF, CLOTH_ARMOR, LEATHER_BOOTS, CLOTH_HOOD, COPPER_RING],
    3:  [COPPER_SWORD, OAK_STAFF, LEATHER_ARMOR, LEATHER_BOOTS, LEATHER_HELMET, RING_VITALITY],
    4:  [COPPER_SWORD, OAK_STAFF, LEATHER_ARMOR, LEATHER_BOOTS, LEATHER_HELMET, RING_VITALITY],
    5:  [IRON_SWORD, ARCANE_STAFF, CHAIN_MAIL, MAGE_ROBE, IRON_BOOTS, ARCANE_HOOD, RING_POWER],
    6:  [IRON_SWORD, ARCANE_STAFF, CHAIN_MAIL, MAGE_ROBE, SWIFT_BOOTS, IRON_HELMET, RING_POWER],
    7:  [IRON_SWORD, ARCANE_STAFF, CHAIN_MAIL, MAGE_ROBE, SWIFT_BOOTS, RING_WARDING],
    8:  [ABYSSAL_BLADE, VOID_STAFF, SHADOW_PLATE, SWIFT_BOOTS, CROWN_OF_ABYSS, RING_WARDING],
    9:  [ABYSSAL_BLADE, VOID_STAFF, SHADOW_PLATE, SHADOW_BOOTS, CROWN_OF_ABYSS, RING_WARDING],
    10: [ABYSSAL_BLADE, VOID_STAFF, SHADOW_PLATE, SHADOW_BOOTS, CROWN_OF_ABYSS, RING_OF_LUCAS],
}

ALL_ITEMS: list[Item] = [
    WOODEN_SWORD, WOODEN_STAFF, COPPER_SWORD, OAK_STAFF,
    IRON_SWORD, ARCANE_STAFF, ABYSSAL_BLADE, VOID_STAFF,
    CLOTH_ARMOR, LEATHER_ARMOR, CHAIN_MAIL, MAGE_ROBE, SHADOW_PLATE,
    CLOTH_HOOD, LEATHER_HELMET, IRON_HELMET, ARCANE_HOOD, CROWN_OF_ABYSS,
    CLOTH_BOOTS, LEATHER_BOOTS, IRON_BOOTS, SWIFT_BOOTS, SHADOW_BOOTS,
    COPPER_RING, RING_VITALITY, RING_POWER, RING_WARDING, RING_OF_LUCAS,
]

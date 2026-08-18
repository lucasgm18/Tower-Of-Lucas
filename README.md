# 🏰 Tower of Lucas

> Um RPG de texto por turnos onde você sobe os 10 andares de uma torre, enfrenta monstros, coleta itens épicos e desafia o próprio Arquiteto — Lucas.

---

## 🎮 Como jogar

```bash
# Clone o repositório
git clone https://github.com/lucasgm18/Tower-Of-Lucas.git
cd Tower-Of-Lucas

# Rode o jogo (Python 3.11+, sem dependências externas)
python3 main.py
```

### Fluxo básico
1. **Crie um personagem** — escolha classe e raça
2. **Suba os andares** — enfrente 3 monstros por andar
3. **Colete itens** — drops com raridades Comum → Épico
4. **Derrote os bosses** — Guardião (andar 5) e Lucas, o Arquiteto (andar 10)

---

## ⚔️ Classes

| Classe | HP | ATK | DEF | VEL | Mana | Skills |
|---|---|---|---|---|---|---|
| **Guerreiro** | 60 | 8 | 5 | 5 | 0 | Golpe Pesado, Postura Defensiva |
| **Mago** | 40 | 5 | 2 | 7 | 30 | Bola de Fogo, Escudo Arcano |

## 🧬 Raças

| Raça | Bônus |
|---|---|
| **Humano** | +1 DEF, +2 VEL, +5 Mana |
| **Orc** | +15 HP, +2 ATK, −1 DEF, −2 VEL, −10 Mana |

---

## 🗂️ Arquitetura

O projeto segue **Object Calisthenics** e está organizado em pacotes com responsabilidades bem definidas:

```
Tower-Of-Lucas/
├── core/               # Lógica de domínio (imutável)
│   ├── character.py    # Entidade principal do jogador
│   ├── stats.py        # Value Object de atributos
│   ├── mana_pool.py    # Value Object de mana (current + maximum)
│   ├── skill_cooldowns.py  # First-class collection de cooldowns
│   ├── combat.py       # Motor de combate com dispatch table
│   ├── exp.py          # Sistema de experiência e level up
│   ├── inventory.py    # Inventário imutável
│   └── items.py        # Item, ItemSlot, Rarity
├── data/               # Dados estáticos (frozen dataclasses)
│   ├── classes.py      # CharacterClass, Skill, SkillType
│   ├── races.py        # Race e bônus por raça
│   ├── monsters.py     # Monstros por andar
│   ├── bosses.py       # Bosses com intro narrativa
│   └── items_db.py     # Banco de itens e drops por andar
├── floors/             # Lógica de progressão de andares
│   └── floor_manager.py
├── ui/                 # Camada de apresentação (isolada do domínio)
│   └── console_ui.py   # Interface de console — pronta para ser trocada
├── persistence/        # Save/load em JSON
│   └── save.py
└── main.py             # Entry point
```

### Princípios aplicados (Object Calisthenics)

| Regra | Aplicação |
|---|---|
| **Wrap primitives** | `mana + max_mana` → `ManaPool` value object |
| **First-class collections** | `dict[str, int]` → `SkillCooldowns` |
| **Sem `else`** | Early returns em todo o fluxo |
| **Polimorfismo** | `if/elif` de skills → `_SKILL_DISPATCH: dict[SkillType, Callable]` |
| **Entidades pequenas** | Cada módulo com responsabilidade única |

---

## 🧪 Testando

```bash
# Smoke test rápido
python3 -c "
from core.character import Character
from data.classes import ALL_CLASSES
from data.races import ALL_RACES
c = Character.create('Teste', ALL_CLASSES['Guerreiro'], ALL_RACES['Humano'])
print(c.summary())
"
```

---

## 🗺️ Roadmap

- [x] Engine de combate por turnos
- [x] Sistema de classes e raças
- [x] Inventário com raridades (Comum → Épico)
- [x] Saves em JSON
- [x] Refatoração com Object Calisthenics
- [ ] Frontend web (FastAPI + React ou Pygame)
- [ ] Mais classes (Ladino, Paladino)
- [ ] Mais raças e monstros
- [ ] Sistema de habilidades passivas

---

## 📜 Licença

MIT © Lucas

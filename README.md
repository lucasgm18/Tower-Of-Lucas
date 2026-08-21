# 🏰 Tower of Lucas

> Um RPG de texto por turnos onde você sobe os 10 andares de uma torre, enfrenta monstros, coleta itens épicos e desafia o próprio Arquiteto — Lucas.

---

## 🎮 Como jogar

### 🖥️ Modo Console (Terminal)
```bash
# Clone o repositório
git clone https://github.com/lucasgm18/Tower-Of-Lucas.git
cd Tower-Of-Lucas

# Rode o jogo no terminal (Python 3.11+)
python3 main.py
```

### 🌐 Modo Servidor API REST (FastAPI)
```bash
# Instale as dependências da API
pip install -r requirements.txt

# Inicie o servidor FastAPI
uvicorn api.app:app --reload
```
Acesse a documentação interativa em **http://127.0.0.1:8000/docs** (Swagger UI).

### 🎨 Modo Frontend Web 2D (React + Vite + Phaser)
```bash
# Em um terminal, inicie a API Python:
uvicorn api.app:app --port 8000

# Em outro terminal, inicie a interface web:
cd frontend
npm install
npm run dev
```
Acesse a arena 2D em **http://localhost:5173**.

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
| **Ladino** | 45 | 7 | 3 | 9 | 15 | Ataque Furtivo, Passo das Sombras |

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
├── api/                    # API REST com FastAPI
│   ├── app.py              # Instância principal FastAPI
│   ├── routes.py           # Endpoints REST (/api/classes, /api/characters)
│   ├── schemas.py          # Schemas Pydantic de requisição/resposta
│   └── tests/
│       └── test_routes.py  # Testes de integração dos endpoints
├── core/                   # Lógica de domínio do jogo
│   ├── character.py        # Entidade principal do jogador
│   ├── stats.py            # Value Object de atributos
│   ├── mana_pool.py        # Value Object de mana
│   ├── skill_cooldowns.py  # Gerenciador de cooldowns
│   ├── combat.py           # Motor de combate e dispatch table
│   ├── exp.py              # Sistema de experiência e level up
│   ├── inventory.py        # Inventário imutável
│   ├── gold.py             # Value Object de ouro
│   └── items.py            # Item, ItemSlot, Rarity
├── data/                   # Dados estáticos do jogo
│   ├── classes.py          # Definição do Ladino, Mago e Guerreiro
│   ├── races.py            # Raças e bônus raciais
│   ├── monsters.py         # Monstros por andar
│   ├── bosses.py           # Bosses com narrativa
│   ├── items_db.py         # Banco de itens e drops
│   └── tests/
│       └── test_rogue_class.py  # Testes da classe Ladino
├── floors/                 # Lógica de progressão e acampamento
│   ├── floor_manager.py
│   └── camp.py
├── persistence/            # Persistência relacional SQLite
│   ├── database.py         # Conexão e schema SQLite
│   ├── save.py             # CRUD de salvamento do jogo
│   └── tests/
│       └── test_sqlite.py  # Testes de persistência SQLite
├── ui/                     # Camada de apresentação de console
│   └── console_ui.py       # Interface de console
└── main.py                 # Entry point do console
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
# Executar todos os testes (co-localizados por módulo)
python3 -m unittest discover -s . -p "test_*.py"

# Smoke test rápido no console
python3 -c "
from core.character import Character
from data.classes import ALL_CLASSES
from data.races import ALL_RACES
c = Character.create('Sombra', ALL_CLASSES['Ladino'], ALL_RACES['Humano'])
print(c.summary())
"
```

---

## 🗺️ Roadmap

- [x] Engine de combate por turnos
- [x] Sistema de classes e raças
- [x] Inventário com raridades (Comum → Épico)
- [x] Refatoração com Object Calisthenics
- [x] Suíte de testes unitários e de API
- [x] Nova classe de personagem (Ladino)
- [x] Persistência relacional em SQLite
- [x] API REST com FastAPI (endpoints OpenAPI/Swagger)
- [ ] Frontend web (React ou Pygame)
- [ ] Mais raças e monstros
- [ ] Sistema de habilidades passivas

---

## 📜 Licença

MIT © Lucas

const API_BASE = '/api';

export async function fetchCharacters() {
  const res = await fetch(`${API_BASE}/characters`);
  if (!res.ok) throw new Error('Falha ao buscar personagens');
  return res.json();
}

export async function createCharacter(name, className, raceName) {
  const res = await fetch(`${API_BASE}/characters`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name,
      class_name: className,
      race_name: raceName,
    }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Falha ao criar personagem');
  }
  return res.json();
}

export async function startCombat(characterName, floor = 1) {
  const res = await fetch(`${API_BASE}/combat/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      character_name: characterName,
      floor,
    }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Falha ao iniciar combate');
  }
  return res.json();
}

export async function executeCombatAction(combatId, actionType, skillName = '') {
  const res = await fetch(`${API_BASE}/combat/action`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      combat_id: combatId,
      action_type: actionType,
      skill_name: skillName,
    }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Falha ao executar acao de combate');
  }
  return res.json();
}

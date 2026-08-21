const API_BASE = '/api';

export async function fetchCharacters() {
  const res = await fetch(`${API_BASE}/characters`);
  if (!res.ok) throw new Error('Falha ao buscar lista de personagens');
  return res.json();
}

export async function fetchClasses() {
  const res = await fetch(`${API_BASE}/classes`);
  if (!res.ok) throw new Error('Falha ao buscar classes');
  return res.json();
}

export async function fetchRaces() {
  const res = await fetch(`${API_BASE}/races`);
  if (!res.ok) throw new Error('Falha ao buscar raças');
  return res.json();
}

export async function fetchCharacterDetails(name) {
  const res = await fetch(`${API_BASE}/characters/${encodeURIComponent(name)}`);
  if (!res.ok) throw new Error('Falha ao buscar detalhes do personagem');
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

export async function deleteCharacter(name) {
  const res = await fetch(`${API_BASE}/characters/${encodeURIComponent(name)}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Falha ao deletar personagem');
  return res.json();
}

export async function startCombat(characterName, floor = null) {
  const bodyData = { character_name: characterName };
  if (floor !== null && floor !== undefined) {
    bodyData.floor = floor;
  }

  const res = await fetch(`${API_BASE}/combat/start`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bodyData),
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
    throw new Error(err.detail || 'Falha ao executar ação de combate');
  }
  return res.json();
}

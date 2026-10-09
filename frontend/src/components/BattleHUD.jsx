import React from 'react';

export default function BattleHUD({
  character,
  monster,
  encounterIndex = 1,
  totalEncounters = 3,
  isBoss = false,
  floorCompleted = false,
  towerCompleted = false,
  onAction,
  isAnimating,
  combatLog,
  isFinished,
  onRestartCombat,
}) {
  if (!character || !monster) return null;

  const skills = character.skills || [];
  const heroHpPct = Math.max(0, Math.min(100, (character.hp / character.max_hp) * 100));
  const monsterHpPct = Math.max(0, Math.min(100, (monster.hp / monster.max_hp) * 100));
  const heroManaPct = character.max_mana > 0
    ? Math.max(0, Math.min(100, (character.mana / character.max_mana) * 100))
    : 0;

  let finishButtonText = `⚔️ Próximo Encontro (Encontro ${encounterIndex + 1}/${totalEncounters})`;
  if (towerCompleted || character.tower_completed) {
    finishButtonText = '🏆 TORRE CONQUISTADA! (Vitória Final)';
  } else if (floorCompleted) {
    finishButtonText = `🎉 Andar ${character.current_floor - 1} Concluído! Próximo Andar`;
  }

  return (
    <div className="hud-panel">
      {/* Linha de Status de Personagens */}
      <div className="status-row">
        {/* Card do Herói */}
        <div className="unit-card">
          <div className="unit-name">
            <span>{character.name}</span>
            <span className="badge">
              {character.class_name} Nível {character.level} (Andar {character.current_floor})
            </span>
          </div>
          <div className="bar-container">
            <div className="bar-fill hp-hero" style={{ width: `${heroHpPct}%` }} />
            <span className="bar-text">HP: {character.hp} / {character.max_hp}</span>
          </div>
          {character.max_mana > 0 && (
            <div className="bar-container">
              <div className="bar-fill mana-hero" style={{ width: `${heroManaPct}%` }} />
              <span className="bar-text">MANA: {character.mana} / {character.max_mana}</span>
            </div>
          )}
        </div>

        {/* Card do Monstro */}
        <div className="unit-card">
          <div className="unit-name">
            <span>{monster.name}</span>
            <span
              className="badge"
              style={{
                borderColor: isBoss ? '#f59e0b' : '#f43f5e',
                color: isBoss ? '#fbbf24' : '#f43f5e',
                background: isBoss ? 'rgba(245,158,11,0.2)' : 'rgba(244,63,94,0.15)',
                fontWeight: isBoss ? 'bold' : 'normal',
              }}
            >
              {isBoss ? '👑 CHEFE DO ANDAR' : `Encontro ${encounterIndex}/${totalEncounters}`}
            </span>
          </div>
          <div className="bar-container">
            <div className="bar-fill hp-enemy" style={{ width: `${monsterHpPct}%` }} />
            <span className="bar-text">HP: {monster.hp} / {monster.max_hp}</span>
          </div>
        </div>
      </div>

      {/* Linha de Ações de Combate */}
      {!isFinished ? (
        <div className="actions-row">
          <button
            className="btn-action"
            disabled={isAnimating}
            onClick={() => onAction('attack')}
          >
            <span>⚔️ Ataque Básico</span>
            <span className="subtext">Dano Físico Padrão</span>
          </button>

          {skills.map((skill) => {
            const hasMana = character.mana >= skill.mana_cost;
            const isReady = skill.is_ready;
            const disabled = isAnimating || !isReady || !hasMana;

            let subtext = skill.mana_cost > 0 ? `Mana: ${skill.mana_cost}` : 'Sem custo';
            if (!isReady) {
              subtext = `Recarga: ${skill.cooldown_remaining}t`;
            } else if (!hasMana) {
              subtext = `Mana Insuf. (${skill.mana_cost})`;
            }

            return (
              <button
                key={skill.name}
                className="btn-action"
                disabled={disabled}
                onClick={() => onAction('skill', skill.name)}
              >
                <span>✨ {skill.name}</span>
                <span className="subtext">{subtext}</span>
              </button>
            );
          })}
        </div>
      ) : (
        <div className="actions-row">
          <button
            className="btn-action"
            style={{ border: '1px solid #fbbf24', background: 'linear-gradient(135deg, #78350f, #451a03)' }}
            disabled={character.tower_completed || towerCompleted}
            onClick={onRestartCombat}
          >
            {finishButtonText}
          </button>
        </div>
      )}

      {/* Log de Combate */}
      <div className="log-box">
        {combatLog.map((log, index) => (
          <div key={index} className="log-entry">
            {log}
          </div>
        ))}
      </div>
    </div>
  );
}

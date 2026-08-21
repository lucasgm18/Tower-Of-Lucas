import React from 'react';

export default function BattleHUD({
  character,
  monster,
  skills,
  onAction,
  isAnimating,
  combatLog,
  isFinished,
  onRestartCombat,
}) {
  if (!character || !monster) return null;

  const heroHpPct = Math.max(0, Math.min(100, (character.hp / character.max_hp) * 100));
  const monsterHpPct = Math.max(0, Math.min(100, (monster.hp / monster.max_hp) * 100));
  const heroManaPct = character.max_mana > 0
    ? Math.max(0, Math.min(100, (character.mana / character.max_mana) * 100))
    : 0;

  return (
    <div className="hud-panel">
      {/* Linha de Status de Personagens */}
      <div className="status-row">
        {/* Card do Herói */}
        <div className="unit-card">
          <div className="unit-name">
            <span>{character.name}</span>
            <span className="badge">{character.class_name} Nível {character.level}</span>
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
            <span className="badge" style={{ borderColor: '#f43f5e', color: '#f43f5e', background: 'rgba(244,63,94,0.15)' }}>
              Inimigo
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
            const disabled = isAnimating || !hasMana;
            return (
              <button
                key={skill.name}
                className="btn-action"
                disabled={disabled}
                onClick={() => onAction('skill', skill.name)}
              >
                <span>✨ {skill.name}</span>
                <span className="subtext">
                  {skill.mana_cost > 0 ? `Mana: ${skill.mana_cost}` : 'Sem custo'}
                </span>
              </button>
            );
          })}
        </div>
      ) : (
        <div className="actions-row">
          <button className="btn-action" style={{ border: '1px solid #fbbf24', background: 'linear-gradient(135deg, #78350f, #451a03)' }} onClick={onRestartCombat}>
            🔄 Próxima Batalha
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

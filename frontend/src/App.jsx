import React, { useState, useEffect } from 'react';
import PhaserGame from './components/PhaserGame';
import BattleHUD from './components/BattleHUD';
import CharacterModal from './components/CharacterModal';
import { fetchCharacters, fetchCharacterDetails, startCombat, executeCombatAction } from './api/client';
import eventBridge from './game/EventBridge';

export default function App() {
  const [characterName, setCharacterName] = useState('');
  const [characterList, setCharacterList] = useState([]);
  const [combatSession, setCombatSession] = useState(null);
  const [characterState, setCharacterState] = useState(null);
  const [monsterState, setMonsterState] = useState(null);
  const [isAnimating, setIsAnimating] = useState(false);
  const [combatLog, setCombatLog] = useState([]);
  const [isFinished, setIsFinished] = useState(false);
  const [floorCompleted, setFloorCompleted] = useState(false);
  const [towerCompleted, setTowerCompleted] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [error, setError] = useState('');

  // 1. Carregar lista de personagens ao montar
  useEffect(() => {
    loadCharacters();
  }, []);

  async function loadCharacters() {
    try {
      const list = await fetchCharacters();
      setCharacterList(list);
      if (list.length > 0 && !characterName) {
        setCharacterName(list[0]);
      } else if (list.length === 0) {
        setShowModal(true);
      }
    } catch (err) {
      setError('Falha ao conectar com o backend Python. Verifique se o server FastAPI está rodando.');
    }
  }

  // 2. Iniciar nova batalha via API
  async function handleStartBattle(selectedName = null) {
    let nameToUse = selectedName || characterName;
    setError('');

    if (!nameToUse) {
      setShowModal(true);
      return;
    }

    try {
      // Omitir andar para que o backend use o character.current_floor oficial
      const session = await startCombat(nameToUse);
      setCombatSession(session);
      setCharacterName(nameToUse);
      setCharacterState(session.character);
      setMonsterState(session.monster);
      setCombatLog([
        `Batalha Iniciada! ${session.monster.name} apareceu no Andar ${session.character.current_floor} (Encontro ${session.encounter_index}/${session.total_encounters}).`,
      ]);
      setIsFinished(false);
      setFloorCompleted(false);
      setTowerCompleted(false);
      setShowModal(false);

      // Emitir evento para o Phaser posicionar sprites
      eventBridge.emit('INIT_BATTLE', session);
    } catch (err) {
      setError(err.message || 'Erro ao iniciar combate.');
    }
  }

  // 3. Executar ação de turno no combate
  async function handleCombatAction(actionType, skillName = '') {
    if (!combatSession || isAnimating || isFinished) return;

    setIsAnimating(true);
    setError('');

    try {
      const res = await executeCombatAction(combatSession.combat_id, actionType, skillName);

      // Atualizar Mana e Skills imediatamente se foi gasto ou recuperado
      if (res.character) {
        setCharacterState((prev) => ({
          ...prev,
          mana: res.character.mana,
          skills: res.character.skills,
        }));
      } else {
        setCharacterState((prev) => ({
          ...prev,
          mana: res.player_mana_after,
        }));
      }

      const onEnemyDamaged = (data) => {
        setMonsterState((prev) => (prev ? { ...prev, hp: data.enemyHp } : null));
      };

      const onHeroDamaged = (data) => {
        setCharacterState((prev) => (prev ? { ...prev, hp: data.heroHp } : null));
      };

      // Esperar animação do Phaser terminar antes de finalizar o turno no HUD React
      const onAnimationDone = () => {
        eventBridge.off('ENEMY_DAMAGED', onEnemyDamaged);
        eventBridge.off('HERO_DAMAGED', onHeroDamaged);
        eventBridge.off('TURN_ANIMATION_COMPLETE', onAnimationDone);

        // Atualizar estado definitivo do personagem e do monstro
        if (res.character) {
          setCharacterState(res.character);
        } else {
          setCharacterState((prev) => ({
            ...prev,
            hp: res.player_hp_after,
            mana: res.player_mana_after,
          }));
        }

        setMonsterState((prev) => ({
          ...prev,
          hp: res.enemy_hp_after,
        }));

        setCombatLog((prev) => [...res.combat_log, ...prev]);

        if (res.victory || res.character_defeated) {
          setIsFinished(true);
          setFloorCompleted(!!res.floor_completed);
          setTowerCompleted(!!res.tower_completed);
        }

        setIsAnimating(false);
      };

      eventBridge.on('ENEMY_DAMAGED', onEnemyDamaged);
      eventBridge.on('HERO_DAMAGED', onHeroDamaged);
      eventBridge.on('TURN_ANIMATION_COMPLETE', onAnimationDone);

      // Emitir animações no Phaser
      eventBridge.emit('PLAY_TURN_ANIMATIONS', res);
    } catch (err) {
      setError(err.message || 'Erro ao processar ação de combate.');
      setIsAnimating(false);
    }
  }

  return (
    <div className="game-container">
      {/* Header com seleção de personagem e controle */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ fontSize: '1.4rem', fontWeight: '800', background: 'linear-gradient(90deg, #fbbf24, #f59e0b)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
          TOWER OF LUCAS 2D
        </h1>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <button
            onClick={() => setShowModal(true)}
            style={{ padding: '6px 12px', borderRadius: '6px', background: '#374151', color: '#fff', border: '1px solid #4b5563', cursor: 'pointer', fontSize: '0.85rem' }}
          >
            👤 {characterName ? `Herói: ${characterName}` : 'Selecionar Herói'}
          </button>

          {!combatSession ? (
            <button
              onClick={() => handleStartBattle()}
              style={{ padding: '8px 16px', borderRadius: '6px', background: '#10b981', color: '#fff', fontWeight: 'bold', border: 'none', cursor: 'pointer' }}
            >
              🚀 Entrar na Batalha
            </button>
          ) : (
            <button
              onClick={() => setCombatSession(null)}
              style={{ padding: '6px 12px', borderRadius: '6px', background: '#374151', color: '#9ca3af', border: 'none', cursor: 'pointer', fontSize: '0.85rem' }}
            >
              ❌ Sair do Combate
            </button>
          )}
        </div>
      </div>

      {error && (
        <div style={{ padding: '10px 14px', borderRadius: '8px', background: 'rgba(244,63,94,0.2)', border: '1px solid #f43f5e', color: '#fecdd3', fontSize: '0.9rem' }}>
          ⚠️ {error}
        </div>
      )}

      {/* Phaser Canvas 2D Game */}
      <PhaserGame />

      {/* React HUD de Combate */}
      {combatSession && (
        <BattleHUD
          character={characterState}
          monster={monsterState}
          encounterIndex={combatSession.encounter_index}
          totalEncounters={combatSession.total_encounters}
          isBoss={combatSession.is_boss}
          floorCompleted={floorCompleted}
          towerCompleted={towerCompleted}
          onAction={handleCombatAction}
          isAnimating={isAnimating}
          combatLog={combatLog}
          isFinished={isFinished}
          onRestartCombat={() => handleStartBattle()}
        />
      )}

      {/* Modal de Criação / Seleção de Personagem */}
      {showModal && (
        <CharacterModal
          onSelectCharacter={(name) => {
            setCharacterName(name);
            handleStartBattle(name);
          }}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  );
}

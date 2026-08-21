import React, { useState, useEffect } from 'react';
import { fetchClasses, fetchRaces, fetchCharacters, createCharacter, deleteCharacter } from '../api/client';

export default function CharacterModal({ onSelectCharacter, onClose }) {
  const [activeTab, setActiveTab] = useState('select'); // 'select' | 'create'
  const [characterList, setCharacterList] = useState([]);
  const [classesList, setClassesList] = useState([]);
  const [racesList, setRacesList] = useState([]);
  
  // State formulário de criação
  const [newName, setNewName] = useState('');
  const [selectedClass, setSelectedClass] = useState('');
  const [selectedRace, setSelectedRace] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    setLoading(true);
    try {
      const [chars, classes, races] = await Promise.all([
        fetchCharacters(),
        fetchClasses(),
        fetchRaces(),
      ]);
      setCharacterList(chars);
      setClassesList(classes);
      setRacesList(races);

      if (classes.length > 0) setSelectedClass(classes[0].name);
      if (races.length > 0) setSelectedRace(races[0].name);

      if (chars.length === 0) {
        setActiveTab('create');
      }
    } catch (err) {
      setError(err.message || 'Erro ao carregar dados do servidor.');
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e) {
    e.preventDefault();
    if (!newName.trim()) {
      setError('Por favor, informe o nome do herói.');
      return;
    }
    setError('');
    setLoading(true);

    try {
      const created = await createCharacter(newName.trim(), selectedClass, selectedRace);
      onSelectCharacter(created.name);
    } catch (err) {
      setError(err.message || 'Erro ao criar personagem.');
      setLoading(false);
    }
  }

  async function handleDelete(charName, e) {
    e.stopPropagation();
    if (!window.confirm(`Deseja realmente excluir o herói "${charName}"?`)) return;

    try {
      await deleteCharacter(charName);
      await loadData();
    } catch (err) {
      setError(err.message || 'Erro ao deletar personagem.');
    }
  }

  const activeClassObj = classesList.find((c) => c.name === selectedClass);
  const activeRaceObj = racesList.find((r) => r.name === selectedRace);

  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <h2>🏰 SELEÇÃO DE HERÓI</h2>
          <div className="tab-group">
            <button
              className={`tab-btn ${activeTab === 'select' ? 'active' : ''}`}
              onClick={() => setActiveTab('select')}
            >
              Heróis Salvos ({characterList.length})
            </button>
            <button
              className={`tab-btn ${activeTab === 'create' ? 'active' : ''}`}
              onClick={() => setActiveTab('create')}
            >
              ➕ Criar Novo
            </button>
          </div>
        </div>

        {error && <div className="modal-error">⚠️ {error}</div>}

        {loading ? (
          <div className="loading-spinner">Carregando dados da torre...</div>
        ) : activeTab === 'select' ? (
          <div className="character-grid">
            {characterList.length === 0 ? (
              <div className="empty-state">
                <p>Nenhum herói encontrado.</p>
                <button className="btn-primary" onClick={() => setActiveTab('create')}>
                  Criar Primeiro Herói
                </button>
              </div>
            ) : (
              characterList.map((name) => (
                <div key={name} className="hero-select-card" onClick={() => onSelectCharacter(name)}>
                  <div className="hero-info">
                    <span className="hero-name">{name}</span>
                    <span className="hero-tag">Aventureiro da Torre</span>
                  </div>
                  <div className="hero-actions">
                    <button className="btn-select">⚔️ Entrar</button>
                    <button className="btn-delete" title="Excluir" onClick={(e) => handleDelete(name, e)}>
                      🗑️
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>
        ) : (
          <form onSubmit={handleCreate} className="create-form">
            <div className="form-group">
              <label>Nome do Herói:</label>
              <input
                type="text"
                placeholder="Ex: Sombra, Valente..."
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                maxLength={30}
              />
            </div>

            <div className="form-row">
              <div className="form-group flex-1">
                <label>Classe:</label>
                <select value={selectedClass} onChange={(e) => setSelectedClass(e.target.value)}>
                  {classesList.map((c) => (
                    <option key={c.name} value={c.name}>
                      {c.name}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group flex-1">
                <label>Raça:</label>
                <select value={selectedRace} onChange={(e) => setSelectedRace(e.target.value)}>
                  {racesList.map((r) => (
                    <option key={r.name} value={r.name}>
                      {r.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Preview de Atributos e Skills */}
            <div className="preview-container">
              {activeClassObj && (
                <div className="preview-card">
                  <h4>Classe: {activeClassObj.name}</h4>
                  <p className="preview-desc">{activeClassObj.description}</p>
                  <div className="stats-badges">
                    <span>HP Base: {activeClassObj.base_hp}</span>
                    <span>ATK: {activeClassObj.base_atk}</span>
                    <span>DEF: {activeClassObj.base_defense}</span>
                    <span>VEL: {activeClassObj.base_speed}</span>
                    <span>Mana: {activeClassObj.base_mana}</span>
                  </div>
                  <h5 style={{ marginTop: '8px', color: '#fbbf24' }}>Habilidades da Classe:</h5>
                  <ul className="skills-list">
                    {activeClassObj.skills.map((s) => (
                      <li key={s.name}>
                        <strong>{s.name}</strong> — {s.description} (Custo: {s.mana_cost} Mana, Recarga: {s.cooldown}t)
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {activeRaceObj && (
                <div className="preview-card">
                  <h4>Bônus da Raça: {activeRaceObj.name}</h4>
                  <p className="preview-desc">{activeRaceObj.description}</p>
                  <div className="stats-badges">
                    {activeRaceObj.hp_bonus !== 0 && <span>HP: {activeRaceObj.hp_bonus > 0 ? `+${activeRaceObj.hp_bonus}` : activeRaceObj.hp_bonus}</span>}
                    {activeRaceObj.atk_bonus !== 0 && <span>ATK: {activeRaceObj.atk_bonus > 0 ? `+${activeRaceObj.atk_bonus}` : activeRaceObj.atk_bonus}</span>}
                    {activeRaceObj.defense_bonus !== 0 && <span>DEF: {activeRaceObj.defense_bonus > 0 ? `+${activeRaceObj.defense_bonus}` : activeRaceObj.defense_bonus}</span>}
                    {activeRaceObj.speed_bonus !== 0 && <span>VEL: {activeRaceObj.speed_bonus > 0 ? `+${activeRaceObj.speed_bonus}` : activeRaceObj.speed_bonus}</span>}
                    {activeRaceObj.mana_bonus !== 0 && <span>Mana: {activeRaceObj.mana_bonus > 0 ? `+${activeRaceObj.mana_bonus}` : activeRaceObj.mana_bonus}</span>}
                  </div>
                </div>
              )}
            </div>

            <div className="modal-actions">
              <button type="submit" className="btn-confirm">
                ⚔️ Confirmar & Iniciar Batalha
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
}

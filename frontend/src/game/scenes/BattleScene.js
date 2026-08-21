import Phaser from 'phaser';
import BattleUnit from '../sprites/BattleUnit';
import eventBridge from '../EventBridge';

export default class BattleScene extends Phaser.Scene {
  constructor() {
    super('BattleScene');
    this.heroUnit = null;
    this.monsterUnit = null;
  }

  create() {
    this._createArenaBackground();

    // Posicionamento inicial dos combatentes
    this.heroUnit = new BattleUnit(this, 200, 260, 'Heroi', true);
    this.monsterUnit = new BattleUnit(this, 600, 260, 'Monstro', false);

    // Escutar eventos do React via EventBridge
    eventBridge.on('INIT_BATTLE', this.handleInitBattle, this);
    eventBridge.on('PLAY_TURN_ANIMATIONS', this.handlePlayTurn, this);

    // Notificar React que a cena está pronta
    eventBridge.emit('PHASER_READY');
  }

  _createArenaBackground() {
    const width = this.cameras.main.width;
    const height = this.cameras.main.height;

    // Fundo Gradiente e Grid
    const graphics = this.add.graphics();
    graphics.fillGradientStyle(0x0a0c10, 0x0a0c10, 0x121620, 0x121620, 1);
    graphics.fillRect(0, 0, width, height);

    // Pedestais de Batalha (Glow Platforms)
    const heroPlatform = this.add.ellipse(200, 310, 140, 40, 0x38bdf8, 0.25);
    const monsterPlatform = this.add.ellipse(600, 310, 140, 40, 0xf43f5e, 0.25);

    this.tweens.add({
      targets: [heroPlatform, monsterPlatform],
      alpha: 0.4,
      duration: 1500,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });

    // Título no Canvas
    this.add.text(width / 2, 35, '— ARENA DE COMBATE 2D —', {
      fontFamily: "'Outfit', sans-serif",
      fontSize: '16px',
      fontWeight: 'bold',
      color: '#40506e',
      letterSpacing: 2,
    }).setOrigin(0.5);
  }

  handleInitBattle(data) {
    if (!data) return;
    const heroName = data.character ? data.character.name : 'Heroi';
    const monsterName = data.monster ? data.monster.name : 'Monstro';

    if (this.heroUnit) this.heroUnit.container.destroy();
    if (this.monsterUnit) this.monsterUnit.container.destroy();

    this.heroUnit = new BattleUnit(this, 200, 260, heroName, true);
    this.monsterUnit = new BattleUnit(this, 600, 260, monsterName, false);
  }

  handlePlayTurn(turnData) {
    const { player_damage_dealt, enemy_damage_dealt, victory } = turnData;

    // 1. Herói ataca
    this.heroUnit.playAttack(600, () => {
      // Impacto no monstro
      this.monsterUnit.playHit(player_damage_dealt);

      // Se a vitória não ocorreu e o monstro contra-ataca
      if (!victory && enemy_damage_dealt >= 0) {
        this.time.delayedCall(400, () => {
          this.monsterUnit.playAttack(200, () => {
            this.heroUnit.playHit(enemy_damage_dealt);
            this.time.delayedCall(400, () => {
              eventBridge.emit('TURN_ANIMATION_COMPLETE');
            });
          });
        });
      } else {
        this.time.delayedCall(500, () => {
          eventBridge.emit('TURN_ANIMATION_COMPLETE');
        });
      }
    });
  }

  destroy() {
    eventBridge.off('INIT_BATTLE', this.handleInitBattle, this);
    eventBridge.off('PLAY_TURN_ANIMATIONS', this.handlePlayTurn, this);
    super.destroy();
  }
}

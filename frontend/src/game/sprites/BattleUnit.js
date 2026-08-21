import Phaser from 'phaser';

export default class BattleUnit {
  /**
   * @param {Phaser.Scene} scene
   * @param {number} x
   * @param {number} y
   * @param {string} name
   * @param {boolean} isPlayer
   * @param {string} [textureKey]
   */
  constructor(scene, x, y, name, isPlayer, textureKey = '') {
    this.scene = scene;
    this.initialX = x;
    this.initialY = y;
    this.name = name;
    this.isPlayer = isPlayer;

    // Se textureKey existir no cache, usa Sprite. Senao, cria Graphics Placeholder.
    if (textureKey && scene.textures.exists(textureKey)) {
      this.container = scene.add.sprite(x, y, textureKey);
    } else {
      this.container = this._createPlaceholderGraphics(x, y);
    }

    this._startIdleAnimation();
  }

  _createPlaceholderGraphics(x, y) {
    const container = this.scene.add.container(x, y);

    const color = this.isPlayer ? 0x38bdf8 : 0xf43f5e;
    const borderColor = this.isPlayer ? 0x0284c7 : 0xbe123c;

    const graphics = this.scene.add.graphics();
    graphics.lineStyle(3, borderColor, 1);
    graphics.fillStyle(color, 0.9);

    if (this.isPlayer) {
      // Formato de Heroi (Escudo / Retangulo Arredondado)
      graphics.fillRoundedRect(-30, -45, 60, 90, 10);
      graphics.strokeRoundedRect(-30, -45, 60, 90, 10);
    } else {
      // Formato de Inimigo (Losango / Monstro)
      graphics.beginPath();
      graphics.moveTo(0, -50);
      graphics.lineTo(35, 0);
      graphics.lineTo(0, 50);
      graphics.lineTo(-35, 0);
      graphics.closePath();
      graphics.fillPath();
      graphics.strokePath();
    }

    // Texto de nome sobre a cabeça
    const nameText = this.scene.add.text(0, -65, this.name, {
      fontFamily: 'Outfit, sans-serif',
      fontSize: '14px',
      fontStyle: 'bold',
      color: '#ffffff',
      stroke: '#000000',
      strokeThickness: 3,
    }).setOrigin(0.5);

    container.add([graphics, nameText]);
    return container;
  }

  _startIdleAnimation() {
    this.idleTween = this.scene.tweens.add({
      targets: this.container,
      scaleY: 1.05,
      y: this.initialY - 3,
      duration: 800,
      yoyo: true,
      repeat: -1,
      ease: 'Sine.easeInOut',
    });
  }

  playAttack(targetX, onComplete) {
    if (this.idleTween) this.idleTween.pause();

    const dir = this.isPlayer ? 1 : -1;
    const strikeX = this.initialX + (dir * 80);

    this.scene.tweens.add({
      targets: this.container,
      x: strikeX,
      duration: 200,
      ease: 'Power2',
      yoyo: true,
      onYoyo: () => {
        if (onComplete) onComplete();
      },
      onComplete: () => {
        this.container.setPosition(this.initialX, this.initialY);
        if (this.idleTween) this.idleTween.resume();
      },
    });
  }

  playHit(damageAmount) {
    // Flash em vermelho
    const targetGraphics = this.container.first || this.container;

    this.scene.tweens.add({
      targets: targetGraphics,
      alpha: 0.3,
      duration: 80,
      yoyo: true,
      repeat: 3,
    });

    // Tremor de impacto
    this.scene.tweens.add({
      targets: this.container,
      x: this.initialX + (this.isPlayer ? -15 : 15),
      duration: 50,
      yoyo: true,
      repeat: 2,
      onComplete: () => {
        this.container.setPosition(this.initialX, this.initialY);
      },
    });

    // Número Flutuante de Dano
    if (damageAmount > 0) {
      this._showFloatingDamageText(damageAmount);
    }
  }

  _showFloatingDamageText(amount) {
    const damageText = this.scene.add.text(
      this.initialX,
      this.initialY - 30,
      `-${amount}`,
      {
        fontFamily: "'Press Start 2P', monospace",
        fontSize: '20px',
        color: this.isPlayer ? '#f43f5e' : '#fbbf24',
        stroke: '#000000',
        strokeThickness: 4,
      }
    ).setOrigin(0.5);

    this.scene.tweens.add({
      targets: damageText,
      y: this.initialY - 80,
      alpha: 0,
      duration: 1000,
      ease: 'Power1',
      onComplete: () => damageText.destroy(),
    });
  }
}

import Phaser from 'phaser';

export default class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
  }

  preload() {
    // Espaço reservado para pré-carregamento de assets de imagens no futuro
  }

  create() {
    this.scene.start('BattleScene');
  }
}

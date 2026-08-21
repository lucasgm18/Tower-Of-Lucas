import Phaser from 'phaser';
import BootScene from './scenes/BootScene';
import BattleScene from './scenes/BattleScene';

export function createPhaserConfig(containerId) {
  return {
    type: Phaser.AUTO,
    parent: containerId,
    width: 800,
    height: 480,
    backgroundColor: '#0d1117',
    scale: {
      mode: Phaser.Scale.FIT,
      autoCenter: Phaser.Scale.CENTER_BOTH,
    },
    scene: [BootScene, BattleScene],
    physics: {
      default: 'arcade',
      arcade: {
        debug: false,
      },
    },
  };
}

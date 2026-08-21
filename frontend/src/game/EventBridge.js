import Phaser from 'phaser';

class EventBridge extends Phaser.Events.EventEmitter {}

export const eventBridge = new EventBridge();
export default eventBridge;

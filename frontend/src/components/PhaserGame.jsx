import React, { useEffect, useRef } from 'react';
import Phaser from 'phaser';
import { createPhaserConfig } from '../game/PhaserConfig';

export default function PhaserGame() {
  const containerRef = useRef(null);
  const gameRef = useRef(null);

  useEffect(() => {
    if (containerRef.current && !gameRef.current) {
      const config = createPhaserConfig(containerRef.current);
      gameRef.current = new Phaser.Game(config);
    }

    return () => {
      if (gameRef.current) {
        gameRef.current.destroy(true);
        gameRef.current = null;
      }
    };
  }, []);

  return (
    <div className="canvas-wrapper">
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
}

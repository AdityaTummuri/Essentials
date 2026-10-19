---
name: browser-audio
description: "Implement interactive Web Audio API soundscapes, spatial 3D audio, user-gesture unlock lifecycles, and audio-reactive WebGL shader visualizers."
---

# Web Audio & Interactive Sound Architecture

Use this skill when building interactive browser soundscapes, game audio, spatial 3D positioning, synthesizer sound effects, or audio-driven WebGL visualizers.

## Core Rules & Architecture

### 1. AudioContext Lifecycle & User-Gesture Unlocking
- Modern browsers suspend new `AudioContext` instances until the user interacts with the page (click, tap, keypress).
- **Graceful Unlock Handler**:
  ```javascript
  let audioCtx = null;

  export function getAudioContext() {
    if (!audioCtx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      audioCtx = new AudioContextClass();
    }
    if (audioCtx.state === 'suspended') {
      const resume = () => {
        audioCtx.resume();
        window.removeEventListener('pointerdown', resume);
        window.removeEventListener('keydown', resume);
      };
      window.addEventListener('pointerdown', resume);
      window.addEventListener('keydown', resume);
    }
    return audioCtx;
  }
  ```

### 2. Spatial 3D Audio (PannerNode)
- Pair sound emitters with Three.js objects using `PannerNode`:
  - Set `panningModel = 'HRTF'` for realistic binaural audio rendering.
  - Set `distanceModel = 'inverse'` with tuned `refDistance` and `maxDistance`.
  - Continuously update the listener position from the active camera transform.

### 3. Audio-Reactive Visualizers (AnalyserNode)
- Connect audio sources to an `AnalyserNode` with `fftSize = 512` or `1024`.
- Extract frequency bins into a `Uint8Array` using `analyser.getByteFrequencyData()`.
- Pass frequency intensities as uniforms (or data textures) into Three.js vertex/fragment shaders to deform meshes or drive particle colors in real time.

### 4. Accessibility & User Controls
- **Global Mute Control**: Always provide a prominent, accessible audio toggle button with `aria-label` and persisted `localStorage` state.
- **Respect User Preferences**: If `prefers-reduced-motion` is enabled, tone down reactive flashing or disorienting low-frequency visual tremors.

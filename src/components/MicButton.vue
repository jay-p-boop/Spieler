<template>
  <button
    id="mic-button"
    class="mic-btn"
    :class="{
      'mic-btn--listening': isListening,
      'mic-btn--success': showSuccess,
      'mic-btn--error': showError,
      'mic-btn--disabled': disabled,
    }"
    :disabled="disabled"
    :aria-label="isListening ? 'Aufnahme läuft' : 'Mikrofon starten'"
    @click="$emit('click')"
  >
    <span v-if="isListening" class="mic-btn__pulse"></span>
    <span v-if="isListening" class="mic-btn__pulse mic-btn__pulse--delayed"></span>

    <!-- Mic icon -->
    <svg v-if="!isListening" class="mic-btn__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <rect x="9" y="1" width="6" height="12" rx="3" />
      <path d="M19 10v1a7 7 0 0 1-14 0v-1" />
      <line x1="12" y1="19" x2="12" y2="23" />
      <line x1="8" y1="23" x2="16" y2="23" />
    </svg>

    <!-- Waveform when listening -->
    <div v-else class="mic-btn__wave">
      <span v-for="i in 5" :key="i" class="mic-btn__wave-bar" :style="{ animationDelay: `${i * 80}ms` }"></span>
    </div>
  </button>
</template>

<script setup>
defineProps({
  isListening: { type: Boolean, default: false },
  showSuccess: { type: Boolean, default: false },
  showError:   { type: Boolean, default: false },
  disabled:    { type: Boolean, default: false },
})
defineEmits(['click'])
</script>

<style scoped>
.mic-btn {
  position: fixed;
  bottom: var(--space-6);
  right: var(--space-6);
  z-index: 1000;
  width: 64px;
  height: 64px;
  border-radius: var(--radius-full);
  border: none;
  background: var(--accent);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  transition: transform var(--duration) var(--ease-out),
              background var(--duration) var(--ease-out),
              box-shadow var(--duration) var(--ease-out);
  -webkit-tap-highlight-color: transparent;
  touch-action: manipulation;
}

.mic-btn:hover:not(:disabled) {
  transform: scale(1.08);
  box-shadow: var(--shadow-lg), 0 0 32px var(--accent-glow);
}

.mic-btn:active:not(:disabled) {
  transform: scale(0.96);
}

.mic-btn--listening {
  background: var(--success);
  box-shadow: var(--shadow-lg), 0 0 24px var(--success-glow);
  animation: glow-breathe 2s ease-in-out infinite;
}

.mic-btn--success {
  background: var(--success);
}

.mic-btn--error {
  background: var(--error);
}

.mic-btn--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.mic-btn__icon {
  width: 24px;
  height: 24px;
}

/* ─── Pulse rings ─── */
.mic-btn__pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: var(--radius-full);
  border: 2px solid var(--success);
  animation: pulse-ring 1.5s ease-out infinite;
}

.mic-btn__pulse--delayed {
  animation-delay: 0.4s;
}

/* ─── Waveform bars ─── */
.mic-btn__wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 24px;
}

.mic-btn__wave-bar {
  width: 3px;
  height: 8px;
  background: white;
  border-radius: 2px;
  animation: wave-bar 0.6s ease-in-out infinite alternate;
}

@keyframes wave-bar {
  0%   { height: 6px; }
  100% { height: 20px; }
}

/* Touch target ≥44px — already 64px */
@media (max-width: 640px) {
  .mic-btn {
    bottom: var(--space-5);
    right: var(--space-5);
    width: 56px;
    height: 56px;
  }
}
</style>

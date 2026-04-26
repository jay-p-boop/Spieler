<template>
  <div class="stats glass" v-if="visible">
    <div class="stats__item">
      <span class="stats__label">Punkte</span>
      <span class="stats__value stats__value--accent">{{ points }}</span>
    </div>
    <div class="stats__divider"></div>
    <div class="stats__item">
      <span class="stats__label">Streak</span>
      <span class="stats__value" :class="{ 'stats__value--fire': streak >= 3 }">
        {{ streak }}{{ streak >= 3 ? ' 🔥' : '' }}
      </span>
    </div>
    <div class="stats__divider"></div>
    <div class="stats__item">
      <span class="stats__label">Fortschritt</span>
      <span class="stats__value">{{ progress }}/{{ total }}</span>
    </div>
    <div class="stats__item stats__item--confidence" v-if="confidence > 0">
      <span class="stats__label">Konfidenz</span>
      <div class="stats__confidence-bar">
        <div class="stats__confidence-fill" :style="{ width: confidence + '%' }" :class="confidenceClass"></div>
      </div>
      <span class="stats__value" style="font-size: var(--text-xs);">{{ confidence }}%</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  points:     { type: Number, default: 0 },
  streak:     { type: Number, default: 0 },
  progress:   { type: Number, default: 0 },
  total:      { type: Number, default: 0 },
  confidence: { type: Number, default: 0 },
  visible:    { type: Boolean, default: true },
})

const confidenceClass = computed(() => {
  if (props.confidence >= 80) return 'stats__confidence-fill--high'
  if (props.confidence >= 50) return 'stats__confidence-fill--mid'
  return 'stats__confidence-fill--low'
})
</script>

<style scoped>
.stats {
  position: fixed;
  top: 56px;
  left: 0;
  right: 0;
  z-index: 899;
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-2) var(--space-5);
  height: 40px;
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: none;
}

.stats__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.stats__item--confidence {
  margin-left: auto;
}

.stats__label {
  font-size: var(--text-xs);
  color: var(--text-muted);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stats__value {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--text-primary);
}

.stats__value--accent {
  color: var(--accent-hover);
}

.stats__value--fire {
  animation: streak-fire 0.8s ease infinite;
}

.stats__divider {
  width: 1px;
  height: 16px;
  background: var(--border);
}

.stats__confidence-bar {
  width: 60px;
  height: 4px;
  background: var(--surface-hover);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.stats__confidence-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.3s var(--ease-out);
}

.stats__confidence-fill--high { background: var(--success); }
.stats__confidence-fill--mid  { background: var(--warning); }
.stats__confidence-fill--low  { background: var(--error); }

@media (max-width: 640px) {
  .stats {
    gap: var(--space-3);
    padding: var(--space-2) var(--space-3);
  }
  .stats__item--confidence { display: none; }
}
</style>

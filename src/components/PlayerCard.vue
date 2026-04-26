<template>
  <div
    :id="`player-${player.Name.replace(/\s/g, '-').toLowerCase()}`"
    class="player-card glass"
    :class="{
      'player-card--correct': isCorrect,
      'player-card--wrong': isWrong,
    }"
  >
    <div class="player-card__image-wrap">
      <img
        :src="player.Bild"
        :alt="player.Name"
        class="player-card__image"
        loading="lazy"
        @error="onImgError"
      />
      <img
        :src="player.Wappen"
        :alt="player.Verein"
        class="player-card__badge"
        loading="lazy"
      />
      <div class="player-card__value-badge">
        {{ player.Marktwert }}
      </div>
    </div>
    <div class="player-card__info">
      <p class="player-card__name">{{ player.Name }}</p>
      <p class="player-card__club">{{ player.Verein }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  player: { type: Object, required: true },
  isCorrect: { type: Boolean, default: false },
  isWrong: { type: Boolean, default: false },
})

function onImgError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect fill="%23141420" width="200" height="200"/><text x="100" y="110" text-anchor="middle" fill="%238b8b9e" font-size="48">⚽</text></svg>'
}
</script>

<style scoped>
.player-card {
  width: 200px;
  overflow: hidden;
  transition: transform var(--duration) var(--ease-out),
              border-color var(--duration) var(--ease-out),
              box-shadow var(--duration) var(--ease-out);
  cursor: default;
  animation: fadeIn 0.4s var(--ease-out) both;
}

.player-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.player-card--correct {
  border-color: var(--success) !important;
  box-shadow: 0 0 24px var(--success-glow);
  animation: success-pop 0.4s var(--ease-out);
}

.player-card--wrong {
  border-color: var(--error) !important;
  box-shadow: 0 0 24px var(--error-glow);
  animation: shake 0.3s ease;
}

.player-card__image-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 3/4;
  background: var(--bg-secondary);
  overflow: hidden;
}

.player-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform var(--duration-slow) var(--ease-out);
}

.player-card:hover .player-card__image {
  transform: scale(1.04);
}

.player-card__badge {
  position: absolute;
  bottom: var(--space-2);
  right: var(--space-2);
  width: 32px;
  height: 32px;
  object-fit: contain;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
}

.player-card__value-badge {
  position: absolute;
  top: var(--space-2);
  left: var(--space-2);
  padding: 2px var(--space-2);
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(8px);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--success);
  letter-spacing: 0.02em;
}

.player-card__info {
  padding: var(--space-3) var(--space-3) var(--space-4);
}

.player-card__name {
  font-size: var(--text-sm);
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.3;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.player-card__club {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>

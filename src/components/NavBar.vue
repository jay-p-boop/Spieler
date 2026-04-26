<template>
  <header class="navbar glass">
    <div class="navbar__brand">
      <img src="/poki.png" alt="Poki" class="navbar__logo" />
      <span class="navbar__title">Poki</span>
      <span class="navbar__season">25/26</span>
    </div>
    <nav class="navbar__tabs" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :id="`tab-${tab.id}`"
        class="navbar__tab"
        :class="{ 'navbar__tab--active': modelValue === tab.id }"
        role="tab"
        :aria-selected="modelValue === tab.id"
        @click="$emit('update:modelValue', tab.id)"
      >
        <span class="navbar__tab-icon">{{ tab.icon }}</span>
        <span class="navbar__tab-label">{{ tab.label }}</span>
      </button>
    </nav>
  </header>
</template>

<script setup>
defineProps({
  modelValue: { type: String, required: true },
})
defineEmits(['update:modelValue'])

const tabs = [
  { id: 'browse', icon: '📋', label: 'Übersicht' },
  { id: 'player-quiz', icon: '🎙️', label: 'Spieler-Quiz' },
  { id: 'club-quiz', icon: '🏟️', label: 'Vereins-Quiz' },
]
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 900;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-5);
  height: 56px;
  border-radius: 0;
  border-top: none;
  border-left: none;
  border-right: none;
}

.navbar__brand {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.navbar__logo {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
}

.navbar__title {
  font-size: var(--text-lg);
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.navbar__season {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--accent);
  background: var(--accent-glow);
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
}

.navbar__tabs {
  display: flex;
  gap: var(--space-1);
}

.navbar__tab {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-3);
  border: none;
  background: transparent;
  color: var(--text-secondary);
  font-family: var(--font);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: all var(--duration) var(--ease-out);
  min-height: 44px; /* WCAG touch target */
}

.navbar__tab:hover {
  color: var(--text-primary);
  background: var(--surface-hover);
}

.navbar__tab--active {
  color: var(--accent-hover);
  background: rgba(99, 102, 241, 0.12);
  font-weight: 600;
}

.navbar__tab-icon {
  font-size: var(--text-base);
}

@media (max-width: 640px) {
  .navbar {
    padding: var(--space-2) var(--space-3);
  }
  .navbar__tab-label {
    display: none;
  }
  .navbar__tab {
    padding: var(--space-2);
  }
  .navbar__title {
    font-size: var(--text-base);
  }
}
</style>

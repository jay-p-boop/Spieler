<template>
  <div class="team-filter" role="listbox" aria-label="Vereinsfilter">
    <button
      class="team-filter__chip"
      :class="{ 'team-filter__chip--active': modelValue === 'all' }"
      @click="$emit('update:modelValue', 'all')"
    >Alle</button>
    <button
      v-for="club in clubs"
      :key="club"
      class="team-filter__chip"
      :class="{ 'team-filter__chip--active': modelValue === club }"
      @click="$emit('update:modelValue', club)"
    >
      <img :src="getWappen(club)" :alt="club" class="team-filter__badge" />
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: String, default: 'all' },
  clubs: { type: Array, required: true },
  wappenMap: { type: Object, required: true },
})
defineEmits(['update:modelValue'])

function getWappen(club) {
  return props.wappenMap[club] || ''
}
</script>

<style scoped>
.team-filter {
  display: flex;
  gap: var(--space-2);
  overflow-x: auto;
  padding: var(--space-3) 0;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.team-filter::-webkit-scrollbar { display: none; }

.team-filter__chip {
  flex-shrink: 0;
  scroll-snap-align: start;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 44px;
  height: 40px;
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  background: var(--surface);
  color: var(--text-secondary);
  font-family: var(--font);
  font-size: var(--text-xs);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--duration) var(--ease-out);
}

.team-filter__chip:hover {
  border-color: var(--border-hover);
  background: var(--surface-hover);
}

.team-filter__chip--active {
  border-color: var(--accent);
  background: rgba(99, 102, 241, 0.12);
  color: var(--accent-hover);
}

.team-filter__badge {
  width: 24px;
  height: 24px;
  object-fit: contain;
}
</style>

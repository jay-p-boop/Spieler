<template>
  <NavBar v-model="activeTab" />
  <StatsBar
    :points="points"
    :streak="streak"
    :progress="learnedCount"
    :total="players.length"
    :confidence="lastConfidence"
    :visible="activeTab !== 'browse'"
  />

  <!-- ─── Browse Mode ─── -->
  <section v-if="activeTab === 'browse'" class="browse-view">
    <TeamFilter
      v-model="selectedClub"
      :clubs="clubNames"
      :wappenMap="wappenMap"
    />
    <div class="player-grid">
      <PlayerCard
        v-for="player in filteredPlayers"
        :key="player.Name"
        :player="player"
        :is-correct="highlightedPlayer === player.Name"
      />
    </div>
  </section>

  <!-- ─── Player Quiz ─── -->
  <section v-if="activeTab === 'player-quiz'" class="quiz-view">
    <div class="quiz-card glass animate-slide-up" v-if="currentPlayer">
      <div class="quiz-card__image-wrap">
        <img :src="proxyImage(currentPlayer.Bild)" :alt="'Quiz'" class="quiz-card__image" referrerpolicy="no-referrer" @error="onImgError" />
        <img :src="proxyImage(currentPlayer.Wappen)" class="quiz-card__badge" referrerpolicy="no-referrer" />
      </div>
      <div class="quiz-card__body">
        <p class="quiz-card__prompt">Wie heißt dieser Spieler?</p>

        <!-- Live transcript -->
        <div class="quiz-card__transcript" v-if="speech.interimTranscript.value || speech.transcript.value">
          <span class="transcript-interim" v-if="speech.interimTranscript.value">{{ speech.interimTranscript.value }}</span>
          <span class="transcript-final" v-if="speech.transcript.value">{{ speech.transcript.value }}</span>
        </div>

        <!-- Feedback -->
        <div v-if="quizFeedback === 'correct'" class="quiz-card__feedback quiz-card__feedback--correct animate-success">
          ✅ Richtig! {{ currentPlayer.Name }}
        </div>
        <div v-if="quizFeedback === 'wrong'" class="quiz-card__feedback quiz-card__feedback--wrong animate-shake">
          ❌ Versuche es nochmal!
        </div>

        <!-- Hint -->
        <div v-if="showHint" class="quiz-card__hint glass">
          💡 Tipp: {{ currentPlayer.Name.charAt(0) }}... ({{ currentPlayer.Verein }})
        </div>

        <!-- Error -->
        <p v-if="speech.error.value" class="quiz-card__error">{{ speech.error.value }}</p>

        <button class="quiz-card__skip" @click="nextQuizPlayer">Überspringen →</button>
      </div>
    </div>
  </section>

  <!-- ─── Club Quiz ─── -->
  <section v-if="activeTab === 'club-quiz'" class="quiz-view">
    <div class="quiz-card glass animate-slide-up" v-if="currentPlayer">
      <div class="quiz-card__body" style="text-align: center;">
        <p class="quiz-card__name-display">{{ currentPlayer.Name }}</p>
        <p class="quiz-card__prompt">Bei welchem Verein spielt er?</p>

        <div class="quiz-card__transcript" v-if="speech.interimTranscript.value || speech.transcript.value">
          <span class="transcript-interim" v-if="speech.interimTranscript.value">{{ speech.interimTranscript.value }}</span>
          <span class="transcript-final" v-if="speech.transcript.value">{{ speech.transcript.value }}</span>
        </div>

        <div v-if="quizFeedback === 'correct'" class="quiz-card__feedback quiz-card__feedback--correct animate-success">
          ✅ Richtig! {{ currentPlayer.Verein }}
        </div>
        <div v-if="quizFeedback === 'wrong'" class="quiz-card__feedback quiz-card__feedback--wrong animate-shake">
          ❌ Versuche es nochmal!
        </div>

        <div v-if="showHint" class="quiz-card__hint glass">
          💡 Tipp: {{ currentPlayer.Verein.charAt(0) }}...
        </div>

        <p v-if="speech.error.value" class="quiz-card__error">{{ speech.error.value }}</p>

        <button class="quiz-card__skip" @click="nextQuizPlayer">Überspringen →</button>
      </div>
    </div>
  </section>

  <MicButton
    :is-listening="speech.isListening.value"
    :show-success="quizFeedback === 'correct'"
    :show-error="quizFeedback === 'wrong'"
    @click="handleMicClick"
  />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from './components/NavBar.vue'
import StatsBar from './components/StatsBar.vue'
import TeamFilter from './components/TeamFilter.vue'
import PlayerCard from './components/PlayerCard.vue'
import MicButton from './components/MicButton.vue'

import { useSpeechRecognition } from './composables/useSpeechRecognition.js'
import { useSpeechSynthesis } from './composables/useSpeechSynthesis.js'
import { usePlayerMatch } from './composables/usePlayerMatch.js'
import { proxyImage } from './composables/useImageProxy.js'

import playersData from './data/players.json'

// ─── State ───
const players = ref(playersData)
const activeTab = ref('browse')
const selectedClub = ref('all')
const points = ref(0)
const streak = ref(0)
const learnedCount = ref(0)
const lastConfidence = ref(0)
const quizFeedback = ref('')   // 'correct' | 'wrong' | ''
const showHint = ref(false)
const consecutiveFails = ref(0)
const currentPlayerIndex = ref(-1)
const highlightedPlayer = ref('')

// ─── Composables ───
const speech = useSpeechRecognition()
const tts = useSpeechSynthesis()
const { findPlayer, findClub, isMatch } = usePlayerMatch(players.value)

// ─── Computed ───
const clubNames = computed(() => {
  return [...new Set(players.value.map(p => p.Verein))].sort()
})

const wappenMap = computed(() => {
  const map = {}
  players.value.forEach(p => { map[p.Verein] = proxyImage(p.Wappen) })
  return map
})

const filteredPlayers = computed(() => {
  if (selectedClub.value === 'all') return players.value
  return players.value.filter(p => p.Verein === selectedClub.value)
})

const currentPlayer = computed(() => {
  if (currentPlayerIndex.value < 0) return null
  return players.value[currentPlayerIndex.value]
})

// ─── Quiz Logic ───
function nextQuizPlayer() {
  quizFeedback.value = ''
  showHint.value = false
  consecutiveFails.value = 0
  lastConfidence.value = 0

  let idx
  do {
    idx = Math.floor(Math.random() * players.value.length)
  } while (idx === currentPlayerIndex.value && players.value.length > 1)

  currentPlayerIndex.value = idx
}

async function handleMicClick() {
  if (speech.isListening.value) {
    speech.stop()
    return
  }

  const result = await speech.listen()
  if (!result) return

  if (activeTab.value === 'browse') {
    // Browse mode: find and highlight player
    const match = findPlayer(result)
    if (match) {
      highlightedPlayer.value = match.player.Name
      lastConfidence.value = match.confidence
      // Scroll to player
      const el = document.getElementById(`player-${match.player.Name.replace(/\s/g, '-').toLowerCase()}`)
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      tts.speak(match.player.Name)
      setTimeout(() => { highlightedPlayer.value = '' }, 3000)
    }
  } else if (activeTab.value === 'player-quiz' && currentPlayer.value) {
    const match = isMatch(result, currentPlayer.value.Name, 60)
    lastConfidence.value = findPlayer(result)?.confidence || 0

    if (match) {
      quizFeedback.value = 'correct'
      streak.value++
      points.value += 10
      learnedCount.value++
      tts.announceCorrect(currentPlayer.value.Name)
      setTimeout(() => nextQuizPlayer(), 1800)
    } else {
      quizFeedback.value = 'wrong'
      streak.value = 0
      consecutiveFails.value++
      tts.announceWrong()
      if (consecutiveFails.value >= 2) showHint.value = true
      setTimeout(() => { quizFeedback.value = '' }, 1500)
    }
  } else if (activeTab.value === 'club-quiz' && currentPlayer.value) {
    const clubMatch = findClub(result)
    lastConfidence.value = clubMatch?.confidence || 0

    if (clubMatch && clubMatch.club === currentPlayer.value.Verein) {
      quizFeedback.value = 'correct'
      streak.value++
      points.value += 5
      learnedCount.value++
      tts.announceClubCorrect(currentPlayer.value.Verein)
      setTimeout(() => nextQuizPlayer(), 1800)
    } else {
      quizFeedback.value = 'wrong'
      streak.value = 0
      consecutiveFails.value++
      tts.announceWrong()
      if (consecutiveFails.value >= 2) showHint.value = true
      setTimeout(() => { quizFeedback.value = '' }, 1500)
    }
  }
}

function onImgError(e) {
  e.target.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 260"><rect fill="%23141420" width="200" height="260"/><text x="100" y="140" text-anchor="middle" fill="%238b8b9e" font-size="48">⚽</text></svg>'
}

// ─── Init ───
onMounted(() => {
  nextQuizPlayer()
})
</script>

<style>
/* ─── Browse View ─── */
.browse-view {
  padding-top: var(--space-4);
}

.player-grid {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
  justify-content: center;
  padding-bottom: 100px;
}

/* ─── Quiz View ─── */
.quiz-view {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: var(--space-7);
  min-height: 60vh;
}

.quiz-card {
  width: 100%;
  max-width: 360px;
  overflow: hidden;
}

.quiz-card__image-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 3/4;
  background: var(--bg-secondary);
  overflow: hidden;
}

.quiz-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.quiz-card__badge {
  position: absolute;
  bottom: var(--space-3);
  right: var(--space-3);
  width: 40px;
  height: 40px;
  object-fit: contain;
  filter: drop-shadow(0 2px 6px rgba(0,0,0,0.6));
}

.quiz-card__body {
  padding: var(--space-5);
}

.quiz-card__prompt {
  font-size: var(--text-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--space-4);
}

.quiz-card__name-display {
  font-size: var(--text-2xl);
  font-weight: 800;
  color: var(--accent-hover);
  margin-bottom: var(--space-3);
}

.quiz-card__transcript {
  margin-bottom: var(--space-3);
  padding: var(--space-3);
  background: var(--surface-hover);
  border-radius: var(--radius-md);
  min-height: 40px;
}

.transcript-interim {
  color: var(--text-muted);
  font-style: italic;
}

.transcript-final {
  color: var(--text-primary);
  font-weight: 600;
}

.quiz-card__feedback {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-weight: 600;
  font-size: var(--text-sm);
  margin-bottom: var(--space-3);
}

.quiz-card__feedback--correct {
  background: rgba(34, 197, 94, 0.12);
  color: var(--success);
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.quiz-card__feedback--wrong {
  background: rgba(239, 68, 68, 0.12);
  color: var(--error);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.quiz-card__hint {
  padding: var(--space-3);
  margin-bottom: var(--space-3);
  font-size: var(--text-sm);
  color: var(--warning);
  border-color: rgba(245, 158, 11, 0.2) !important;
}

.quiz-card__error {
  color: var(--error);
  font-size: var(--text-sm);
  margin-bottom: var(--space-3);
}

.quiz-card__skip {
  width: 100%;
  padding: var(--space-3);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  background: transparent;
  color: var(--text-secondary);
  font-family: var(--font);
  font-size: var(--text-sm);
  font-weight: 500;
  cursor: pointer;
  transition: all var(--duration) var(--ease-out);
  min-height: 44px;
}

.quiz-card__skip:hover {
  border-color: var(--border-hover);
  color: var(--text-primary);
  background: var(--surface-hover);
}

@media (max-width: 640px) {
  .quiz-card {
    max-width: 100%;
    border-radius: var(--radius-lg);
  }
}
</style>

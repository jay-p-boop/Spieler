/**
 * useSpeechSynthesis — SOTA Text-to-Speech Output
 * Uses browser-native Web Speech Synthesis API
 * Auto-selects best German voice
 */
import { ref, onMounted } from 'vue'

export function useSpeechSynthesis() {
  const isSpeaking = ref(false)
  const voices = ref([])
  const selectedVoice = ref(null)
  const rate = ref(1.0)
  const pitch = ref(1.0)

  const synth = window.speechSynthesis

  function loadVoices() {
    const allVoices = synth.getVoices()
    // Prefer German voices, ranked by quality
    const deVoices = allVoices.filter(v => v.lang.startsWith('de'))

    // Priority: Google > Microsoft > Apple > Others
    const ranked = deVoices.sort((a, b) => {
      const score = (v) => {
        if (v.name.includes('Google')) return 4
        if (v.name.includes('Microsoft') && v.name.includes('Neural')) return 3
        if (v.name.includes('Anna') || v.name.includes('Petra')) return 2 // Apple
        return 1
      }
      return score(b) - score(a)
    })

    voices.value = ranked
    selectedVoice.value = ranked[0] || allVoices[0] || null
  }

  onMounted(() => {
    loadVoices()
    if (synth.onvoiceschanged !== undefined) {
      synth.onvoiceschanged = loadVoices
    }
  })

  /**
   * Speak text aloud
   */
  function speak(text, options = {}) {
    if (!synth || !text) return

    // Cancel any ongoing speech
    synth.cancel()

    const utterance = new SpeechSynthesisUtterance(text)
    utterance.lang = 'de-DE'
    utterance.rate = options.rate || rate.value
    utterance.pitch = options.pitch || pitch.value
    utterance.volume = options.volume ?? 1.0

    if (selectedVoice.value) {
      utterance.voice = selectedVoice.value
    }

    utterance.onstart = () => { isSpeaking.value = true }
    utterance.onend = () => { isSpeaking.value = false }
    utterance.onerror = () => { isSpeaking.value = false }

    synth.speak(utterance)
  }

  /**
   * Pre-built feedback phrases
   */
  function announceCorrect(playerName) {
    speak(`Richtig! ${playerName}`, { rate: 1.1 })
  }

  function announceWrong() {
    speak('Leider falsch. Versuch es nochmal!', { rate: 1.0 })
  }

  function announceHint(playerName, club) {
    speak(`Der gesuchte Spieler ist ${playerName} von ${club}.`, { rate: 0.9 })
  }

  function announceClubCorrect(clubName) {
    speak(`Richtig! ${clubName}!`, { rate: 1.1 })
  }

  function stop() {
    synth?.cancel()
    isSpeaking.value = false
  }

  return {
    isSpeaking,
    voices,
    selectedVoice,
    rate,
    pitch,
    speak,
    stop,
    announceCorrect,
    announceWrong,
    announceHint,
    announceClubCorrect,
  }
}

/**
 * useSpeechRecognition — SOTA Speech Recognition
 * Uses Web Speech API (free, browser-native, no API key)
 * Supports interim results, confidence scoring, German language
 */
import { ref, onUnmounted } from 'vue'

export function useSpeechRecognition() {
  const isListening = ref(false)
  const transcript = ref('')
  const interimTranscript = ref('')
  const confidence = ref(0)
  const error = ref('')
  const isSupported = ref(false)

  let recognition = null
  let timeoutId = null

  // ─── Detect Support ───
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  isSupported.value = !!SpeechRecognition

  /**
   * Start listening with Web Speech API
   */
  async function listen() {
    if (isListening.value) return null

    if (!SpeechRecognition) {
      error.value = 'Spracherkennung wird in diesem Browser nicht unterstützt. Bitte Chrome oder Edge nutzen.'
      return null
    }

    return new Promise((resolve) => {
      recognition = new SpeechRecognition()
      recognition.lang = 'de-DE'
      recognition.continuous = false
      recognition.interimResults = true
      recognition.maxAlternatives = 3

      recognition.onstart = () => {
        isListening.value = true
        error.value = ''
        transcript.value = ''
        interimTranscript.value = ''
        confidence.value = 0
      }

      recognition.onresult = (event) => {
        let interim = ''
        let final = ''

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i]
          if (result.isFinal) {
            final += result[0].transcript
            confidence.value = Math.round(result[0].confidence * 100)
          } else {
            interim += result[0].transcript
          }
        }

        if (final) {
          transcript.value = cleanTranscript(final)
          resolve(transcript.value)
        }
        interimTranscript.value = interim
      }

      recognition.onerror = (event) => {
        isListening.value = false
        if (event.error === 'no-speech') {
          error.value = 'Keine Sprache erkannt. Versuche es nochmal.'
        } else if (event.error === 'not-allowed') {
          error.value = 'Mikrofon-Zugriff verweigert. Bitte erlaube den Zugriff in den Browser-Einstellungen.'
        } else if (event.error === 'network') {
          error.value = 'Netzwerkfehler bei der Spracherkennung.'
        } else {
          error.value = `Fehler: ${event.error}`
        }
        resolve(null)
      }

      recognition.onend = () => {
        isListening.value = false
        clearTimeout(timeoutId)
        if (!transcript.value) resolve(null)
      }

      // Timeout safety net
      timeoutId = setTimeout(() => {
        if (recognition) {
          recognition.stop()
          if (!transcript.value) {
            error.value = 'Zeitüberschreitung — bitte sprich deutlicher.'
          }
        }
      }, 8000)

      try {
        recognition.start()
      } catch (e) {
        error.value = 'Spracherkennung konnte nicht gestartet werden.'
        resolve(null)
      }
    })
  }

  function stop() {
    clearTimeout(timeoutId)
    if (recognition) {
      recognition.stop()
      recognition = null
    }
    isListening.value = false
  }

  function cleanTranscript(text) {
    return text
      .toLowerCase()
      .trim()
      .replace(/\.$/, '')      // trailing period
      .replace(/\s+/g, ' ')    // normalize spaces
  }

  onUnmounted(() => stop())

  return {
    isListening,
    transcript,
    interimTranscript,
    confidence,
    error,
    isSupported,
    listen,
    stop,
  }
}

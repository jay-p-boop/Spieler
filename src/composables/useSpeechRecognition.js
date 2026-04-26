/**
 * useSpeechRecognition — SOTA Dual-Stack Speech Recognition
 * Primary: Web Speech API (free, browser-native)
 * Fallback: Azure Cognitive Services Speech SDK
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
  let azureRecognizer = null
  let timeoutId = null

  // ─── Detect Support ───
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  isSupported.value = !!SpeechRecognition

  /**
   * Start listening with Web Speech API (primary)
   */
  function startWebSpeech() {
    return new Promise((resolve) => {
      if (!SpeechRecognition) {
        error.value = 'Web Speech API nicht unterstützt'
        resolve(null)
        return
      }

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
          error.value = 'Mikrofon-Zugriff verweigert. Bitte erlaube den Zugriff.'
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

  /**
   * Start listening with Azure Speech SDK (fallback)
   */
  async function startAzureSpeech() {
    const key = import.meta.env.VITE_AZURE_SPEECH_KEY
    const region = import.meta.env.VITE_AZURE_SPEECH_REGION || 'westeurope'

    if (!key) {
      error.value = 'Azure Speech Key nicht konfiguriert.'
      return null
    }

    try {
      const SpeechSDK = await import('microsoft-cognitiveservices-speech-sdk')
      const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(key, region)
      speechConfig.speechRecognitionLanguage = 'de-DE'
      const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput()
      azureRecognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig)

      return new Promise((resolve) => {
        isListening.value = true
        error.value = ''
        transcript.value = ''

        timeoutId = setTimeout(() => {
          azureRecognizer?.stopContinuousRecognitionAsync()
          error.value = 'Zeitüberschreitung'
          isListening.value = false
          resolve(null)
        }, 10000)

        azureRecognizer.recognizeOnceAsync(
          (result) => {
            clearTimeout(timeoutId)
            isListening.value = false
            if (result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
              transcript.value = cleanTranscript(result.text)
              confidence.value = 85 // Azure doesn't expose confidence easily
              resolve(transcript.value)
            } else {
              error.value = 'Keine Sprache erkannt.'
              resolve(null)
            }
          },
          (err) => {
            clearTimeout(timeoutId)
            isListening.value = false
            error.value = `Azure Fehler: ${err}`
            resolve(null)
          }
        )
      })
    } catch (e) {
      error.value = 'Azure SDK konnte nicht geladen werden.'
      return null
    }
  }

  /**
   * Main entry: try Web Speech first, fall back to Azure
   */
  async function listen() {
    if (isListening.value) return null

    if (isSupported.value) {
      return startWebSpeech()
    } else {
      return startAzureSpeech()
    }
  }

  function stop() {
    clearTimeout(timeoutId)
    if (recognition) {
      recognition.stop()
      recognition = null
    }
    if (azureRecognizer) {
      azureRecognizer.stopContinuousRecognitionAsync()
      azureRecognizer = null
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

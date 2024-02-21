 listenToPokemonName() {
      if (this.micButtonDisabled) {
        return;
      }
      this.isListening = true;
      this.micButtonDisabled = true;

      // Erstellen des SpeechRecognizer
      const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
      const recognizer = new SpeechSDK.SpeechRecognizer(this.speechConfig, audioConfig);

      recognizer.recognizeOnceAsync(result => {
        this.isListening = false;
        this.micButtonDisabled = false;

        if (result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
          const spokenWord = result.text.toLowerCase().trim();
          alert("Erkannter Text: " + spokenWord);
          const closestPokemon = thion(spokenWord);
          this.recognizedText = closestPokemon.name;
          // ... restliche Logik ...
        } else {
          alert("Spracherkennung fehlgeschlagen: " + result.reason);
        }
      });

      // Timeout-Logik, falls benötigt
      // ...
    },
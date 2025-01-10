<template>
  <div id="app" role="application">
    <button
      class="floating-mic"
      :class="{ listening: isListening }"
      :disabled="micButtonDisabled"
      @click="listenToName"
      aria-label="Spielernamen oder Vereinsnamen erkennen"
      aria-live="polite"
    >
      <div v-if="isListening" class="pulse" aria-hidden="true"></div>
      <span aria-hidden="true">🎤</span>
    </button>

    <div class="app-bar" role="navigation">
      <button
        class="tab-button"
        :class="{ 'active-tab': !learningMode && !clubLearningMode }"
        @click="stopLearningMode"
        role="button"
        aria-label="Startseite"
      >
        🏠 Start
      </button>
      <button
        class="tab-button"
        :class="{ 'active-tab': learningMode }"
        @click="startLearningMode"
        role="button"
        aria-label="Spieler lernen Modus"
      >
        📚 Spieler Lernen
      </button>
      <button
        class="tab-button"
        :class="{ 'active-tab': clubLearningMode }"
        @click="startClubLearningMode"
        role="button"
        aria-label="Vereine lernen Modus"
      >
        📚 Vereine Lernen
      </button>
    </div>

    <div class="player-card" v-if="learningMode" role="dialog" aria-labelledby="player-question">
      <div class="image-container">
        <img
          :src="currentLearningPlayer.image"
          :class="{ 'correct-answer': correctPlayerIndex === currentLearningIndex }"
          @click="speakPlayerName(currentLearningPlayer.name)"
          :alt="'Spielerbild von ' + currentLearningPlayer.name"
        />
        <img
          :src="currentLearningPlayer.wappen"
          :alt="'Vereinswappen von ' + currentLearningPlayer.verein"
          class="club-badge"
          @click.stop="speakClubName(currentLearningPlayer.verein)"
        />
      </div>
      <p id="player-question">Wie heißt dieser Spieler?</p>

      <button class="button-80" @click="showNextPlayer" role="button">Weiter</button>
      <p>Erkannter Text: <span aria-live="polite">{{ recognizedText }}</span></p>
      <p v-if="errorMessage" class="error-message" aria-live="assertive">Fehler: {{ errorMessage }}</p> 
    </div>

    <div class="player-card" v-if="clubLearningMode" role="dialog" aria-labelledby="club-question">
      <img
        :src="currentLearningPlayer.wappen"
        :class="{ 'correct-answer': correctPlayerIndex === currentLearningIndex }"
        @click="speakClubName(currentLearningPlayer.verein)"
        :alt="'Vereinswappen von ' + currentLearningPlayer.verein"
      />
      <p id="club-question">Wie heißt dieser Verein?</p>

      <button class="button-80" @click="showNextClub" role="button">Weiter</button>
      <p>Erkannter Text: <span aria-live="polite">{{ recognizedText }}</span></p>
      <p v-if="errorMessage" class="error-message" aria-live="assertive">Fehler: {{ errorMessage }}</p>
      <div v-if="guessedClubs.length > 0" class="guessed-clubs">
        <h3>Bereits erratene Vereine:</h3>
        <ul v-if="!showAllClubs">
          <li v-for="club in guessedClubs.slice(0, 5)" :key="club">
            {{ club }} ✔️
          </li>
        </ul>
        <ul v-else>
          <li v-for="club in guessedClubs" :key="club">
            {{ club }} ✔️
          </li>
        </ul>
        <button v-if="guessedClubs.length > 5 && !showAllClubs" @click="showAllClubs = true">Mehr anzeigen</button>
        <button v-else-if="showAllClubs" @click="showAllClubs = false">Weniger anzeigen</button>
      </div>
    </div>

    <div v-if="!learningMode && !clubLearningMode">
      <div class="player-row" v-for="player in players" :key="player.name">
        <div
          class="player-card"
          @click="speakPlayerName(player.name)"
          :ref="`player-${player.name.toLowerCase().replace(/\s/g, '')}`"
          tabindex="0"
          :aria-label="'Spielerkarte für ' + player.name + ', Position: ' + player.position + ', Alter: ' + player.age + ', Marktwert: ' + player.marketValue"
        >
          <div class="image-container">
            <img :src="player.image" :alt="'Spielerbild von ' + player.name" class="player-image" />
            <img
              :src="player.wappen"
              :alt="'Vereinswappen von ' + player.verein"
              class="club-badge"
              @click.stop="speakClubName(player.verein)"
            />
          </div>
          <p class="player-nummer">{{ player.nummer }}</p>
          <p class="player-name">{{ player.name }}</p>
          <p class="player-info">Position: {{ player.position }}</p>
          <p class="player-info">Alter: {{ player.age }} Jahre</p>
          <p class="player-info">Marktwert: {{ player.marketValue }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
#app {
  text-align: center;
  background-color: #f6f6f6;
  padding-top: 70px;
}

.app-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  background-color: grey;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.tab-button {
  background-color: transparent;
  color: #fff;
  border: none;
  font-size: 16px;
  font-weight: bold;
  padding: 10px;
  cursor: pointer;
  outline: none;
}

.active-tab {
  border-bottom: 2px solid #1899d6;
}

.button-19 {
  appearance: button;
  background-color: #1899d6;
  border: solid transparent;
  border-radius: 16px;
  border-width: 0 0 4px;
  box-sizing: border-box;
  color: #ffffff;
  cursor: pointer;
  display: inline-block;
  font-family: din-round, sans-serif;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.8px;
  line-height: 20px;
  margin: 0;
  outline: none;
  overflow: visible;
  padding: 13px 16px;
  text-align: center;
  text-transform: uppercase;
  touch-action: manipulation;
  transform: translatez(0);
  transition: filter 0.2s;
  user-select: none;
  -webkit-user-select: none;
  vertical-align: middle;
  white-space: nowrap;
  width: 100%;
}

.button-19:after {
  background-clip: padding-box;
  background-color: #1cb0f6;
  border: solid transparent;
  border-radius: 16px;
  border-width: 0 0 4px;
  bottom: -4px;
  content: "";
  left: 0;
  position: absolute;
  right: 0;
  top: 0;
  z-index: -1;
}

.button-19:main,
.button-19:focus {
  user-select: auto;
}

.button-19:hover:not(:disabled) {
  filter: brightness(1.1);
  -webkit-filter: brightness(1.1);
}

.button-19:disabled {
  cursor: auto;
}

.button-80 {
  background: #fff;
  backface-visibility: hidden;
  border-radius: 0.375rem;
  border-style: solid;
  border-width: 0.125rem;
  box-sizing: border-box;
  color: #212121;
  cursor: pointer;
  display: inline-block;
  font-family: Circular, Helvetica, sans-serif;
  font-size: 1.125rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  line-height: 1.3;
  padding: 0.875rem 1.125rem;
  position: relative;
  text-align: left;
  text-decoration: none;
  transform: translatez(0) scale(1);
  transition: transform 0.2s;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.button-80:not(:disabled):hover {
  transform: scale(1.05);
}

.button-80:not(:disabled):hover:active {
  transform: scale(1.05) translatey(0.125rem);
}

.button-80:focus {
  outline: 0 solid transparent;
}

.button-80:focus:before {
  content: "";
  left: calc(-1 * 0.375rem);
  pointer-events: none;
  position: absolute;
  top: calc(-1 * 0.375rem);
  transition: border-radius;
  user-select: none;
}

.button-80:focus:not(:focus-visible) {
  outline: 0 solid transparent;
}

.button-80:focus:not(:focus-visible):before {
  border-width: 0;
}

.button-80:not(:disabled):active {
  transform: translatey(0.125rem);
}

.player-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 30px;
}

.player-card {
  background-color: #ffffff;
  border: 1px solid #ddd;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  overflow: hidden;
  text-align: center;
  margin: 10px;
  width: 250px;
}

.player-card img {
  width: 100%;
  height: auto;
  /*border-bottom: 1px solid #ddd;*/
}

.player-card .club-badge {
  position: absolute;
  bottom: 10px;
  /* Abstand vom unteren Rand des Spielerbildes */
  right: 10px;
  /* Abstand vom rechten Rand des Spielerbildes */
  width: 25%;
  /* Stellen Sie die Größe nach Bedarf ein */
}

.player-card p {
  margin: 10px 0;
}

.player-card .player-name {
  font-size: 18px;
  font-weight: bold;
  color: #004d99;
}

.player-card .player-info {
  font-size: 14px;
  color: #666;
}

.correct-answer {
  border: 3px solid #00ff00;
  /* Grün */
}

.button-24 {
  background: #ff4742;
  border: 1px solid #ff4742;
  border-radius: 6px;
  box-shadow: rgba(0, 0, 0, 0.1) 1px 2px 4px;
  box-sizing: border-box;
  color: #ffffff;
  cursor: pointer;
  display: inline-block;
  font-family: nunito, roboto, proxima-nova, "proxima nova", sans-serif;
  font-size: 16px;
  font-weight: 800;
  line-height: 16px;
  min-height: 56px;
  outline: 0;
  padding: 12px 14px;
  text-align: center;
  text-rendering: geometricprecision;
  text-transform: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
}

.button-24:hover,
.button-24:active {
  background-color: initial;
  background-position: 0 0;
  color: #ff4742;
}

.button-24:active {
  opacity: 0.5;
}

.player-nummer {
  font-size: 18px;
  font-weight: bold;
  color: #000;
}

.floating-mic {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  /* Stellen Sie sicher, dass der Button immer im Vordergrund ist */
  background-color: #f44336;
  /* Roter Hintergrund */
  color: white;
  /* Weißer Text */
  border: none;
  border-radius: 50%;
  /* Kreisförmiger Button */
  width: 60px;
  height: 60px;
  font-size: 24px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
  /* Ein bisschen Schatten für den 3D-Effekt */
}

.floating-mic.listening {
  background-color: #4caf50;
  /* Grün, um zu signalisieren, dass es zuhört */
}

.pulse {
  position: absolute;
  border: 5px solid #aaffaa;
  /* Leichtere grüne Farbe */
  border-radius: 50%;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  animation: pulse-animation 0.999s infinite;
}

body {
  font-family: "Roboto", sans-serif;
  background-color: #f0f0f0;
  color: #333;
}

#app {
  background-color: #ffffff;
}

@keyframes pulse-animation {
  0% {
    transform: scale(1);
    opacity: 0.5;
  }

  100% {
    transform: scale(1.85);
    opacity: 0;
  }
}

.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}

.guessed-clubs {
  margin-top: 20px;
}

.guessed-clubs ul {
  list-style: none;
  padding: 0;
}

.guessed-clubs li {
  margin-bottom: 5px;
}
</style>

<script>
import levenshtein from "fast-levenshtein";
import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk";

export default {
  data() {
    return {
      players: [], // Initialisiere das Array als leer
      learningMode: false,
      clubLearningMode: false,
      currentLearningPlayer: null,
      currentLearningIndex: null,
      recognizedText: "",
      successSound: new Audio("assets/success.mp3"), // Pfad zur Erfolgs-Sounddatei
      wrongSound: new Audio("assets/wrong.mp3"), // Pfad zur Fehler-Sounddatei
      correctPlayerIndex: null,
      permissionGranted: false,
      micButtonDisabled: false,
      isListening: false,
      guessedClubs: [],
      errorMessage: "",
      showAllClubs: false
    };
  },
  async created() {
    // Spielerdaten aus der JSON-Datei laden
    try {
      const response = await fetch('jsonspieler.json');
      const playersData = await response.json();

      this.players = playersData.map((player) => {
        const nameLine = player.Name.split('\n').find(line => line.trim() !== '');
        const positionLine = player.Position.split('\n').reverse().find(line => line.trim() !== '');
        const birthdateMatch = player.Geburtsdatum.match(/(.+) \((\d+)\)/);
  
        return {
          name: nameLine ? nameLine.trim() : '',
          position: positionLine ? positionLine.trim() : '',
          birthdate: birthdateMatch ? birthdateMatch[1] : '',
          age: birthdateMatch ? birthdateMatch[2] : '',
          marketValue: player.Marktwert.trim(),
          image: player.Bild,
          verein: player.Verein,
          nummer: player.Nummer,
          wappen: player.Wappen
        };
      });
    } catch (error) {
      console.error("Fehler beim Laden der Spielerdaten:", error);
      this.errorMessage = "Fehler beim Laden der Spielerdaten.";
    }

    navigator.permissions.query({ name: 'microphone' }).then(permissionStatus => {
      this.permissionGranted = permissionStatus.state === 'granted';
      permissionStatus.onchange = () => {
        this.permissionGranted = permissionStatus.state === 'granted';
      };
    });
  },
  methods: {
    speakMessage(message) {
      const speech = new SpeechSynthesisUtterance(message);
      speech.lang = 'de-DE'; // Sprache auf Deutsch setzen
      window.speechSynthesis.speak(speech);
    },
    speakPlayerName(name) {
      this.speakMessage(name);
    },
    speakClubName(clubName) {
      this.speakMessage(clubName);
    },
    startLearningMode() {
      this.resetQuizState();
      this.currentLearningIndex = Math.floor(Math.random() * this.players.length);
      this.currentLearningPlayer = this.players[this.currentLearningIndex];
      this.learningMode = true;
      this.clubLearningMode = false;
    },
    startClubLearningMode() {
      this.resetQuizState();
      this.showNextClub();
      this.clubLearningMode = true;
      this.learningMode = false;
    },
    stopLearningMode() {
      this.learningMode = false;
      this.clubLearningMode = false;
      this.currentLearningPlayer = null;
      this.currentLearningIndex = null;
      this.guessedClubs = [];
      this.recognizedText = "";
      this.errorMessage = "";
    },
    scrollToPlayer(playerName) {
      const cleanPlayerName = playerName.trim().replace(/\.$/, '').toLowerCase();
      const refName = `player-${cleanPlayerName.replace(/\s/g, '')}`;
      if (this.$refs[refName]) {
        const element = this.$refs[refName][0];
        element.scrollIntoView({ behavior: 'smooth' });
      } else {
        console.error('Keine Referenz gefunden für:', cleanPlayerName);
      }
    },
    findClosestPlayer(spokenWord) {
      let closestPlayer = null;
      let smallestDistance = Infinity;

      this.players.forEach(player => {
        let playerName = player.name.toLowerCase();
        let distance = levenshtein.get(spokenWord, playerName);

        if (distance < smallestDistance) {
          smallestDistance = distance;
          closestPlayer = player;
        }
      });

      return closestPlayer;
    },
    findClosestClub(spokenWord) {
      let closestClub = null;
      let smallestDistance = Infinity;

      this.players.forEach(player => {
        let clubName = player.verein.toLowerCase();
        let distance = levenshtein.get(spokenWord, clubName);

        if (distance < smallestDistance) {
          smallestDistance = distance;
          closestClub = player;
        }
      });

      return closestClub;
    },
    showNextPlayer() {
      this.resetQuizState();
      let newIndex;
      do {
        newIndex = Math.floor(Math.random() * this.players.length);
      } while (newIndex === this.currentLearningIndex);
      this.currentLearningIndex = newIndex;
      this.currentLearningPlayer = this.players[this.currentLearningIndex];
    },
    showNextClub() {
      this.resetQuizState();
      if (this.guessedClubs.length === this.players.length) {
        alert("Alle Vereine wurden erraten!");
        this.stopLearningMode();
        return;
      }
      let newIndex;
      do {
        newIndex = Math.floor(Math.random() * this.players.length);
      } while (this.guessedClubs.includes(this.players[newIndex].verein));
      this.currentLearningIndex = newIndex;
      this.currentLearningPlayer = this.players[this.currentLearningIndex];
    },
    listenToName() {
      if (this.micButtonDisabled || !this.permissionGranted) {
        if (!this.permissionGranted) {
            this.errorMessage = "Bitte erlaube den Zugriff auf das Mikrofon in den Browser-Einstellungen.";
        }
        return;
      }
      this.isListening = true;
      this.micButtonDisabled = true;
      this.recognizedText = "";
      this.errorMessage = "";

      const speechConfig = SpeechSDK.SpeechConfig.fromSubscription("901e7cb5bc09481abf6dd507019a3f35", "westeurope");
      speechConfig.speechRecognitionLanguage = 'de-DE';
      const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
      const recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);

      let recognitionTimeout = setTimeout(() => {
        recognizer.stopContinuousRecognitionAsync();
        this.errorMessage = "Zeitüberschreitung: Keine Sprache erkannt.";
        this.isListening = false;
        this.micButtonDisabled = false;
      }, 10000);

      recognizer.recognizeOnceAsync(result => {
        clearTimeout(recognitionTimeout);
        this.isListening = false;
        this.micButtonDisabled = false;

        if (result.reason === SpeechSDK.ResultReason.RecognizedSpeech) {
          const spokenWord = result.text.toLowerCase().trim().replace(/\.$/, '');
          this.recognizedText = spokenWord;

          if (this.learningMode) {
            const closestPlayer = this.findClosestPlayer(spokenWord);
            if (closestPlayer && closestPlayer.name === this.currentLearningPlayer.name) {
              this.correctPlayerIndex = this.currentLearningIndex;
              this.successSound.play();
              setTimeout(() => {
                this.showNextPlayer();
              }, 1000);
            } else {
              this.wrongSound.play();
              this.errorMessage = "Versuche es nochmal!";
            }
          } else if (this.clubLearningMode) {
            const closestClub = this.findClosestClub(spokenWord);
            if (closestClub && closestClub.verein === this.currentLearningPlayer.verein) {
              this.correctPlayerIndex = this.currentLearningIndex;
              this.guessedClubs.push(this.currentLearningPlayer.verein);
              this.successSound.play();
              setTimeout(() => {
                this.showNextClub();
              }, 1000);
            } else {
              this.wrongSound.play();
              this.errorMessage = "Versuche es nochmal!";
            }
          } else {
            const closestPlayer = this.findClosestPlayer(spokenWord);
            if (closestPlayer) {
              this.scrollToPlayer(closestPlayer.name);
            }
          }
        } else {
          this.errorMessage = "Spracherkennung fehlgeschlagen. Bitte versuche es erneut.";
        }
      },
      error => {
          clearTimeout(recognitionTimeout);
          this.isListening = false;
          this.micButtonDisabled = false;
          this.errorMessage = "Fehler bei der Spracherkennung: " + error;
          console.error(error);
      });
    },
    resetQuizState() {
      this.correctPlayerIndex = null;
      this.recognizedText = "";
      this.errorMessage = "";
    }
  }
};
</script>

<template>
  <div id="app">
    <button 
      class="floating-mic" 
      :class="{ 'listening': isListening }" 
      :disabled="micButtonDisabled"
      @click="listenToName"
    >
      <div v-if="isListening" class="pulse"></div>
      🎤
    </button>

    <!-- App Bar am unteren Rand des Bildschirms -->
    <div class="app-bar">
      <button 
        class="tab-button" 
        :class="{ 'active-tab': !learningMode && !clubLearningMode }" 
        @click="stopLearningMode"
      >
        🏠 Start
      </button>
      <button 
        class="tab-button" 
        :class="{ 'active-tab': learningMode }" 
        @click="startLearningMode"
      >
        📚 Spieler Lernen
      </button>
      <button 
        class="tab-button" 
        :class="{ 'active-tab': clubLearningMode }" 
        @click="startClubLearningMode"
      >
        📚 Vereine Lernen
      </button>
    </div>

    <!-- Spielernamen-Lernmodus -->
    <div class="player-card" v-if="learningMode">
      <div class="image-container">
        <img 
          :src="currentLearningPlayer.image" 
          :class="{ 'correct-answer': correctPlayerIndex === currentLearningIndex }" 
          @click="speakPlayerName(currentLearningPlayer.name)" 
          alt="Learning Player Image" 
        />
        <img 
          :src="currentLearningPlayer.wappen" 
          alt="Player Badge" 
          class="club-badge" 
          @click.stop="speakClubName(currentLearningPlayer.verein)" 
        />
      </div>
      <p>Wie heißt dieser Spieler?</p>

      <button class="button-80" @click="showNextPlayer">Weiter</button>
      <p>Erkannter Text: {{ recognizedText }}</p>
    </div>

    <!-- Vereinsnamen-Lernmodus -->
    <div class="player-card" v-if="clubLearningMode">
      <img 
        :src="currentLearningPlayer.wappen" 
        :class="{ 'correct-answer': correctPlayerIndex === currentLearningIndex }" 
        @click="speakClubName(currentLearningPlayer.verein)" 
        alt="Learning Club Badge" 
      />
      <p>Wie heißt dieser Verein?</p>

      <button class="button-80" @click="showNextClub">Weiter</button>
      <p>Erkannter Text: {{ recognizedText }}</p>
    </div>

    <!-- Standardansicht -->
    <div v-if="!learningMode && !clubLearningMode">      
      <div class="player-row" v-for="player in players" :key="player.name">
        <div class="player-card" @click="speakPlayerName(player.name)" :ref="`player-${player.name.toLowerCase().replace(/\s/g, '')}`">
          <div class="image-container">
            <img :src="player.image" alt="Player Image" class="player-image" />
            <img :src="player.wappen" alt="Player Badge" class="club-badge" @click.stop="speakClubName(player.verein)"  />
          </div>
          <p class="player-nummer">{{ player.nummer }}</p>
          <p class="player-name">{{ player.name }}</p>
          <p class="player-info">Position: {{ player.position }}</p>
          <p class="player-info">Alter: {{ player.age }} Jahre</p>
          <p class="player-info">Marktwert: {{ player.marketValue }}</p>
        </div>
      </div>
    </div>

    <!-- Bereits erratene Vereine -->
    <div v-if="clubLearningMode && guessedClubs.length > 0" class="guessed-clubs">
      <h3>Bereits erratene Vereine:</h3>
      <ul>
        <li v-for="club in guessedClubs" :key="club">
          {{ club }} ✔️
        </li>
      </ul>
    </div>
  </div>
</template>








<style>



#app {
  text-align: center;
  background-color: #f6f6f6;  
  padding-top: 20px;
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
    box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
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
    border-bottom: 2px solid #1899D6;
  }
  .button-19 {
    appearance: button;
    background-color: #1899D6;
    border: solid transparent;
    border-radius: 16px;
    border-width: 0 0 4px;
    box-sizing: border-box;
    color: #FFFFFF;
    cursor: pointer;
    display: inline-block;
    font-family: din-round,sans-serif;
    font-size: 15px;
    font-weight: 700;
    letter-spacing: .8px;
    line-height: 20px;
    margin: 0;
    outline: none;
    overflow: visible;
    padding: 13px 16px;
    text-align: center;
    text-transform: uppercase;
    touch-action: manipulation;
    transform: translateZ(0);
    transition: filter .2s;
    user-select: none;
    -webkit-user-select: none;
    vertical-align: middle;
    white-space: nowrap;
    width: 100%;
  }

  .button-19:after {
    background-clip: padding-box;
    background-color: #1CB0F6;
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
    border-radius: .375rem;
    border-style: solid;
    border-width: .125rem;
    box-sizing: border-box;
    color: #212121;
    cursor: pointer;
    display: inline-block;
    font-family: Circular,Helvetica,sans-serif;
    font-size: 1.125rem;
    font-weight: 700;
    letter-spacing: -.01em;
    line-height: 1.3;
    padding: .875rem 1.125rem;
    position: relative;
    text-align: left;
    text-decoration: none;
    transform: translateZ(0) scale(1);
    transition: transform .2s;
    user-select: none;
    -webkit-user-select: none;
    touch-action: manipulation;
  }

  .button-80:not(:disabled):hover {
    transform: scale(1.05);
  }

  .button-80:not(:disabled):hover:active {
    transform: scale(1.05) translateY(.125rem);
  }

  .button-80:focus {
    outline: 0 solid transparent;
  }

  .button-80:focus:before {
    content: "";
    left: calc(-1*.375rem);
    pointer-events: none;
    position: absolute;
    top: calc(-1*.375rem);
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
    transform: translateY(.125rem);
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
  bottom: 10px; /* Abstand vom unteren Rand des Spielerbildes */
  right: 10px; /* Abstand vom rechten Rand des Spielerbildes */
  width: 60px; /* Stellen Sie die Größe nach Bedarf ein */
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
    border: 3px solid #00FF00; /* Grün */
  }

   .button-24 {
     background: #FF4742;
     border: 1px solid #FF4742;
     border-radius: 6px;
     box-shadow: rgba(0, 0, 0, 0.1) 1px 2px 4px;
     box-sizing: border-box;
     color: #FFFFFF;
     cursor: pointer;
     display: inline-block;
     font-family: nunito,roboto,proxima-nova,"proxima nova",sans-serif;
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
     color: #FF4742;
   }

   .button-24:active {
     opacity: .5;
   }
 .player-nummer{
   font-size: 18px;
   font-weight: bold;
   color: #000;
 }


  .floating-mic {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000; /* Stellen Sie sicher, dass der Button immer im Vordergrund ist */
  background-color: #F44336; /* Roter Hintergrund */
  color: white; /* Weißer Text */
  border: none;
  border-radius: 50%; /* Kreisförmiger Button */
  width: 60px;
  height: 60px;
  font-size: 24px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3); /* Ein bisschen Schatten für den 3D-Effekt */
}
  .floating-mic.listening {
  background-color: #4CAF50;  /* Grün, um zu signalisieren, dass es zuhört */
}

  .pulse {
    position: absolute;
    border: 5px solid #aaffaa; /* Leichtere grüne Farbe */
    border-radius: 50%;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    animation: pulse-animation 0.999s infinite;
  }
  body {
    font-family: 'Roboto', sans-serif;
    background-color: #f0f0f0;
    color: #333;
  }
  #app {
    background-color: #ffffff;
  }

  @keyframes pulse-animation {
    0% { transform: scale(1); opacity: 0.5; }
    100% { transform: scale(1.85); opacity: 0; }
  }


</style>


<script>
import levenshtein from 'fast-levenshtein';
import playersData from './jsonspieler.json'; 
import successSoundPath from '@/assets/success.mp3';
import wrongSoundPath from '@/assets/wrong.mp3';
import doubleMetaphonePackage from 'doublemetaphone';
import * as SpeechSDK from 'microsoft-cognitiveservices-speech-sdk';

export default {
  data() {
    return {
      players: playersData.map(player => ({
        name: player.Name.trim().split('\n').find(line => line.trim() !== ''),
        position: player.Position.split('\n').reverse().find(line => line.trim() !== ''),
        birthdate: player.Geburtsdatum.split(" ")[0],
        age: player.Geburtsdatum.match(/\((\d+)\)/)[1],
        marketValue: player.Marktwert.trim(),
        image: player.Bild,
        verein: player.Verein,
        nummer: player.Nummer,
        wappen: player.Wappen
      })),
      learningMode: false,
      clubLearningMode: false,
      currentLearningPlayer: null,
      currentLearningIndex: null,
      recognizedText: "",
      successSound: new Audio(successSoundPath),
      wrongSound: new Audio(wrongSoundPath),
      correctPlayerIndex: null,
      permissionGranted: false,
      micButtonDisabled: false,
      encoder: new doubleMetaphonePackage(),
      isListening: false,
      guessedClubs: [] // Neu: Liste der bereits erratenen Vereine
    };
  },
  created() {
    navigator.permissions.query({ name: 'microphone' }).then(permissionStatus => {
      this.permissionGranted = permissionStatus.state === 'granted';
    });
  },
  methods: {
    speakMessage(message) {
      const speech = new SpeechSynthesisUtterance(message);
      window.speechSynthesis.speak(speech);
    },
    speakPlayerName(name) {
      this.speakMessage(name);
    },
    speakClubName(clubName) {
      this.speakMessage(clubName);
    },
    startLearningMode() {
      this.currentLearningIndex = Math.floor(Math.random() * this.players.length);
      this.currentLearningPlayer = this.players[this.currentLearningIndex];
      this.learningMode = true;
      this.clubLearningMode = false;
    },
    startClubLearningMode() {
      this.showNextClub(); // Initiales Anzeigen eines Vereins
      this.clubLearningMode = true;
      this.learningMode = false;
    },
    stopLearningMode() {
      this.learningMode = false;
      this.clubLearningMode = false;
      this.currentLearningPlayer = null;
      this.currentLearningIndex = null;
      this.guessedClubs = []; // Zurücksetzen der erratenen Vereine
    },
    scrollToPlayer(playerName) {
      // Entfernen von Leerzeichen und Punkten am Ende des Strings
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
      let newIndex;
      do {
        newIndex = Math.floor(Math.random() * this.players.length);
      } while (newIndex === this.currentLearningIndex);
      this.currentLearningIndex = newIndex;
      this.currentLearningPlayer = this.players[this.currentLearningIndex];
      this.correctPlayerIndex = null; // Zurücksetzen des korrekten Spielerindex
    },
    showNextClub() {
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
      this.correctPlayerIndex = null; // Zurücksetzen des korrekten Vereinsindex
    },
    listenToName() {
      if (this.micButtonDisabled) {
        return;
      }
      this.isListening = true;
      this.micButtonDisabled = true;

      const speechConfig = SpeechSDK.SpeechConfig.fromSubscription("901e7cb5bc09481abf6dd507019a3f35", "westeurope");
      speechConfig.speechRecognitionLanguage = 'de-DE';
      const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput();
      const recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig);

      recognizer.recognizeOnceAsync(result => {
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
            }
          } else if (this.clubLearningMode) {
            const closestClub = this.findClosestClub(spokenWord);
            if (closestClub && closestClub.verein === this.currentLearningPlayer.verein) {
              this.correctPlayerIndex = this.currentLearningIndex;
              this.guessedClubs.push(this.currentLearningPlayer.verein); // Hinzufügen des erratenen Vereins zur Liste
              this.successSound.play();
              setTimeout(() => {
                this.showNextClub();
              }, 1000);
            } else {
              this.wrongSound.play();
            }
          } else {
            // Logik für den normalen Modus
            const closestPlayer = this.findClosestPlayer(spokenWord);
            if (closestPlayer) {
              this.scrollToPlayer(closestPlayer.name);
            }
          }
        } else {
          alert("Spracherkennung fehlgeschlagen: " + result.reason);
        }
      });
    },
  }
};
</script>

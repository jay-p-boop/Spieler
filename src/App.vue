<template> <div id="app" role="application"> <!-- Fortschritts- und Punkteanzeige (Feature 1+2) --> <header class="stats-bar"> <div class="progress-info"> <strong>Gelernt:</strong> {{ playersLearnedCount }}/{{ totalPlayersCount }} </div> <div class="score-info"> <strong>Punkte:</strong> {{ totalPoints }} </div> </header>
javascript


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
    ⬅ Start
  </button>
  <button
    class="tab-button"
    :class="{ 'active-tab': learningMode }"
    @click="startLearningMode"
    role="button"
    aria-label="Spieler lernen Modus"
  >
    🏃 Spieler Lernen
  </button>
  <button
    class="tab-button"
    :class="{ 'active-tab': clubLearningMode }"
    @click="startClubLearningMode"
    role="button"
    aria-label="Vereine lernen Modus"
  >
    🏆 Vereine Lernen
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

  <!-- Kontextueller Tipp (Feature 3) -->
  <div v-if="hintVisible" class="hint-box">
    Tipp: Versuche, den Namen deutlich auszusprechen. Die korrekte Aussprache ist z.B. <em>{{ currentLearningPlayer.name }}</em>.
  </div>

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

  <!-- Kontextueller Tipp (Feature 3) -->
  <div v-if="hintVisible" class="hint-box">
    Tipp: Konzentriere dich auf die Vereinsbezeichnung. Hier: <em>{{ currentLearningPlayer.verein }}</em>.
  </div>

  <button class="button-80" @click="showNextClub" role="button">Weiter</button>
  <p>Erkannter Text: <span aria-live="polite">{{ recognizedText }}</span></p>
  <p v-if="errorMessage" class="error-message" aria-live="assertive">Fehler: {{ errorMessage }}</p>
  <div v-if="guessedClubs.length > 0" class="guessed-clubs">
    <h3>Bereits erratene Vereine:</h3>
    <ul v-if="!showAllClubs">
      <li v-for="club in guessedClubs.slice(0, 5)" :key="club">
        {{ club }} ✅
      </li>
    </ul>
    <ul v-else>
      <li v-for="club in guessedClubs" :key="club">
        {{ club }} ✅
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
</div> </template> <script> import levenshtein from "fast-levenshtein"; import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk"; export default { data() { return { players: [], learningMode: false, clubLearningMode: false, currentLearningPlayer: null, currentLearningIndex: null, recognizedText: "", successSound: new Audio("assets/success.mp3"), wrongSound: new Audio("assets/wrong.mp3"), /* (4) Erweiterte Audio-Feedbacks: neues Sound-Ereignis bei mehreren korrekten Antworten */ streakSound: new Audio("assets/streak.mp3"), correctPlayerIndex: null, permissionGranted: false, micButtonDisabled: false, isListening: false, guessedClubs: [], errorMessage: "", showAllClubs: false, /* (1) Personalisierte Fortschrittsanzeige */ playersLearnedCount: 0, totalPlayersCount: 0, /* (2) Gamification: Punkte-System */ totalPoints: 0, /* (3) Kontextuelle Tipps: wird angezeigt, wenn der Nutzer 2x hintereinander falsch liegt */ consecutiveFails: 0, hintVisible: false }; }, async created() { try { const response = await fetch("jsonspieler.json"); const playersData = await response.json(); this.players = playersData.map((player) => { const nameLine = player.Name.split("\n").find((line) => line.trim() !== ""); const positionLine = player.Position.split("\n").reverse().find((line) => line.trim() !== ""); const birthdateMatch = player.Geburtsdatum.match(/(.+) $(\d+)$/); return { name: nameLine ? nameLine.trim() : "", position: positionLine ? positionLine.trim() : "", birthdate: birthdateMatch ? birthdateMatch[1] : "", age: birthdateMatch ? birthdateMatch[2] : "", marketValue: player.Marktwert.trim(), image: player.Bild, verein: player.Verein, nummer: player.Nummer, wappen: player.Wappen }; }); /* Gesamte Spielerzahl für Fortschrittsberechnung */ this.totalPlayersCount = this.players.length; } catch (error) { console.error("Fehler beim Laden der Spielerdaten:", error); this.errorMessage = "Fehler beim Laden der Spielerdaten."; } navigator.permissions.query({ name: "microphone" }).then((permissionStatus) => { this.permissionGranted = permissionStatus.state === "granted"; permissionStatus.onchange = () => { this.permissionGranted = permissionStatus.state === "granted"; }; }); }, methods: { speakMessage(message) { const speech = new SpeechSynthesisUtterance(message); speech.lang = "de-DE"; window.speechSynthesis.speak(speech); }, speakPlayerName(name) { this.speakMessage(name); }, speakClubName(clubName) { this.speakMessage(clubName); }, startLearningMode() { this.resetQuizState(); this.currentLearningIndex = Math.floor(Math.random() * this.players.length); this.currentLearningPlayer = this.players[this.currentLearningIndex]; this.learningMode = true; this.clubLearningMode = false; }, startClubLearningMode() { this.resetQuizState(); this.showNextClub(); this.clubLearningMode = true; this.learningMode = false; }, stopLearningMode() { this.learningMode = false; this.clubLearningMode = false; this.currentLearningPlayer = null; this.currentLearningIndex = null; this.guessedClubs = []; this.recognizedText = ""; this.errorMessage = ""; this.hintVisible = false; }, scrollToPlayer(playerName) { const cleanPlayerName = playerName.trim().replace(/\.$/, "").toLowerCase(); const refName = `player-${cleanPlayerName.replace(/\s/g, "")}`; if (this.$refs[refName]) { const element = this.$refs[refName][0]; element.scrollIntoView({ behavior: "smooth" }); } else { console.error("Keine Referenz gefunden für:", cleanPlayerName); } }, findClosestPlayer(spokenWord) { let closestPlayer = null; let smallestDistance = Infinity; this.players.forEach((player) => { let playerName = player.name.toLowerCase(); let distance = levenshtein.get(spokenWord, playerName); if (distance < smallestDistance) { smallestDistance = distance; closestPlayer = player; } }); return closestPlayer; }, findClosestClub(spokenWord) { let closestClub = null; let smallestDistance = Infinity; this.players.forEach((player) => { let clubName = player.verein.toLowerCase(); let distance = levenshtein.get(spokenWord, clubName); if (distance < smallestDistance) { smallestDistance = distance; closestClub = player; } }); return closestClub; }, showNextPlayer() { this.resetQuizState(); let newIndex; do { newIndex = Math.floor(Math.random() * this.players.length); } while (newIndex === this.currentLearningIndex); this.currentLearningIndex = newIndex; this.currentLearningPlayer = this.players[this.currentLearningIndex]; }, showNextClub() { this.resetQuizState(); if (this.guessedClubs.length === this.players.length) { alert("Alle Vereine wurden erraten!"); this.stopLearningMode(); return; } let newIndex; do { newIndex = Math.floor(Math.random() * this.players.length); } while (this.guessedClubs.includes(this.players[newIndex].verein)); this.currentLearningIndex = newIndex; this.currentLearningPlayer = this.players[this.currentLearningIndex]; }, listenToName() { if (this.micButtonDisabled || !this.permissionGranted) { if (!this.permissionGranted) { this.errorMessage = "Bitte erlaube den Zugriff auf das Mikrofon in den Browser-Einstellungen."; } return; } this.isListening = true; this.micButtonDisabled = true; this.recognizedText = ""; this.errorMessage = ""; this.hintVisible = false; // Tipp ausblenden, wenn Aufnahme neu gestartet wird const speechConfig = SpeechSDK.SpeechConfig.fromSubscription("901e7cb5bc09481abf6dd507019a3f35", "westeurope"); speechConfig.speechRecognitionLanguage = "de-DE"; const audioConfig = SpeechSDK.AudioConfig.fromDefaultMicrophoneInput(); const recognizer = new SpeechSDK.SpeechRecognizer(speechConfig, audioConfig); let recognitionTimeout = setTimeout(() => { recognizer.stopContinuousRecognitionAsync(); this.errorMessage = "Zeitüberschreitung: Keine Sprache erkannt."; this.isListening = false; this.micButtonDisabled = false; this.increaseFail(); }, 10000); recognizer.recognizeOnceAsync( (result) => { clearTimeout(recognitionTimeout); this.isListening = false; this.micButtonDisabled = false; if (result.reason === SpeechSDK.ResultReason.RecognizedSpeech) { const spokenWord = result.text.toLowerCase().trim().replace(/\.$/, ""); this.recognizedText = spokenWord; if (this.learningMode) { const closestPlayer = this.findClosestPlayer(spokenWord); if (closestPlayer && closestPlayer.name === this.currentLearningPlayer.name) { this.handleCorrect(); /* Spieler-Fortschritt (Feature 1) */ this.playersLearnedCount++; /* (2) Punktevergabe */ this.totalPoints += 10; /* Bei einer Streak von 3 korrekten Antworten zusätzliches Audio-Feedback */ if (this.totalPoints % 30 === 0) { this.streakSound.play(); } setTimeout(() => { this.showNextPlayer(); }, 1000); } else { this.handleWrong(); } } else if (this.clubLearningMode) { const closestClub = this.findClosestClub(spokenWord); if (closestClub && closestClub.verein === this.currentLearningPlayer.verein) { this.handleCorrect(); if (!this.guessedClubs.includes(this.currentLearningPlayer.verein)) { this.guessedClubs.push(this.currentLearningPlayer.verein); } this.totalPoints += 5; /* Bei einer Streak von 3 korrekten Antworten zusätzliches Audio-Feedback */ if (this.totalPoints % 15 === 0) { this.streakSound.play(); } setTimeout(() => { this.showNextClub(); }, 1000); } else { this.handleWrong(); } } else { const closestPlayer = this.findClosestPlayer(spokenWord); if (closestPlayer) { this.scrollToPlayer(closestPlayer.name); } } } else { this.errorMessage = "Spracherkennung fehlgeschlagen. Bitte versuche es erneut."; this.increaseFail(); } }, (error) => { clearTimeout(recognitionTimeout); this.isListening = false; this.micButtonDisabled = false; this.errorMessage = "Fehler bei der Spracherkennung: " + error; console.error(error); this.increaseFail(); } ); }, /* Wiederverwendbare Helfer für richtig/falsch (Feature 4: Audio-Feedback) */ handleCorrect() { this.correctPlayerIndex = this.currentLearningIndex; this.successSound.play(); this.consecutiveFails = 0; }, handleWrong() { this.wrongSound.play(); this.errorMessage = "Versuche es nochmal!"; this.increaseFail(); }, increaseFail() { this.consecutiveFails++; /* Kontextueller Tipp nach 2 Fehlschlägen in Folge (Feature 3) */ if (this.consecutiveFails >= 2) { this.hintVisible = true; } }, resetQuizState() { this.correctPlayerIndex = null; this.recognizedText = ""; this.errorMessage = ""; this.consecutiveFails = 0; this.hintVisible = false; } } }; </script> <style> #app { text-align: center; background-color: #f6f6f6; padding-top: 70px; } .stats-bar { position: fixed; top: 50px; left: 0; right: 0; height: 40px; background-color: #eeeeee; display: flex; justify-content: space-between; align-items: center; padding: 0 15px; z-index: 999; } .progress-info, .score-info { font-size: 14px; } .app-bar { position: fixed; top: 90px; left: 0; right: 0; height: 50px; background-color: grey; display: flex; justify-content: space-around; align-items: center; box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1); z-index: 998; } .tab-button { background-color: transparent; color: #fff; border: none; font-size: 16px; font-weight: bold; padding: 10px; cursor: pointer; outline: none; } .active-tab { border-bottom: 2px solid #1899d6; } .button-80 { background: #fff; backface-visibility: hidden; border-radius: 0.375rem; border-style: solid; border-width: 0.125rem; box-sizing: border-box; color: #212121; cursor: pointer; display: inline-block; font-size: 1.125rem; font-weight: 700; margin-top: 20px; padding: 0.875rem 1.125rem; position: relative; text-align: center; text-decoration: none; transform: translateZ(0) scale(1); transition: transform 0.2s; user-select: none; } .button-80:not(:disabled):hover { transform: scale(1.05); } .button-80:not(:disabled):hover:active { transform: scale(1.05) translateY(0.125rem); } .button-80:focus { outline: 0 solid transparent; } .button-80:not(:disabled):active { transform: translateY(0.125rem); } .player-row { display: flex; flex-wrap: wrap; justify-content: center; margin-bottom: 30px; margin-top: 160px; /* Platz schaffen für die fixed Bars */ } .player-card { background-color: #ffffff; border: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); border-radius: 10px; overflow: hidden; text-align: center; margin: 10px; width: 250px; position: relative; } .player-card img { width: 100%; height: auto; } .player-card .club-badge { position: absolute; bottom: 10px; right: 10px; width: 25%; } .player-card p { margin: 10px 0; } .player-card .player-name { font-size: 18px; font-weight: bold; color: #004d99; } .player-card .player-info { font-size: 14px; color: #666; } .correct-answer { border: 3px solid #00ff00; } .floating-mic { position: fixed; bottom: 20px; right: 20px; z-index: 1000; background-color: #f44336; color: white; border: none; border-radius: 50%; width: 60px; height: 60px; font-size: 24px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); } .floating-mic.listening { background-color: #4caf50; } .pulse { position: absolute; border: 5px solid #aaffaa; border-radius: 50%; width: 100%; height: 100%; top: 0; left: 0; animation: pulse-animation 1s infinite; } @keyframes pulse-animation { 0% { transform: scale(1); opacity: 0.5; } 100% { transform: scale(1.85); opacity: 0; } } .error-message { color: red; font-weight: bold; margin-top: 10px; } .guessed-clubs { margin-top: 20px; } .guessed-clubs ul { list-style: none; padding: 0; } .guessed-clubs li { margin-bottom: 5px; } .hint-box { margin: 10px auto; padding: 10px; background-color: #fef8c7; color: #333; border: 1px dashed #ccc; max-width: 80%; text-align: left; } </style>

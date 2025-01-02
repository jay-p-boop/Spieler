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
        <div
          class="player-card"
          @click="speakPlayerName(player.name)"
          :ref="`player-${player.name.toLowerCase().replace(/\s/g, '')}`"
        >
          <div class="image-container">
            <img :src="player.image" alt="Player Image" class="player-image" />
            <img
              :src="player.wappen"
              alt="Player Badge"
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
  color: #ffff;
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
  transform: translateZ(0);
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
  content: '';
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
  transform: translateZ(0) scale(1);
  transition: transform 0.2s;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
}

.button-80:not(:disabled):hover {
  transform: scale(1.05);
}

.button-80:not(:disabled):hover:active {
  transform: scale(1.05) translateY(0.125rem);
}

.button-80:focus {
  outline: 0 solid transparent;
}

.button-80:focus:before {
  content: '';
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
  transform: translateY(0.125rem);
}

.player-row {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 30px;
}

.player-card {
  background-color: #ffff;
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
  border: 3px solid #00ff00; /* Grün */
}

.button-24 {
  background: #ff4742;
  border: 1px solid #ff4742;
  border-radius: 6px;
  box-shadow: rgba(0, 0, 0, 0.1) 1px 2px 4px;
  box-sizing: border-box;
  color: #ffff;
  cursor: pointer;
  display: inline-block;
  font-family: nunito, roboto, proxima-nova, 'proxima nova', sans-serif;
  font-size: 16px;
  font-weight: 800;
  line-height: 16px;

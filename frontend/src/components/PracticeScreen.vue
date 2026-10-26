<script setup>
import { computed } from "vue";
import AnswerCard from "./AnswerCard.vue";
import HintStack from "./HintStack.vue";
import {
  loadQuestion,
  nextQuestion,
  requestHint,
  store,
  submitAnswer,
} from "../store";
import { speakQuestion, speech, stopSpeech } from "../speech";

const cardClass = computed(() => {
  if (!store.verdict || typeof store.verdict !== "object") return "";
  return store.verdict.correct ? "is-right" : "is-wrong";
});
const hasAnswer = computed(() => store.selected !== null);
const solved = computed(() => store.verdict?.correct === true);
const revealed = computed(() => store.verdict?.revealed === true);
const done = computed(() => solved.value || revealed.value);

function toggleReadAloud() {
  if (speech.speaking) {
    stopSpeech();
    return;
  }
  speakQuestion(store.question.text);
}
</script>

<template>
  <section class="card" :class="cardClass" :key="store.question?.id ?? 'empty'">
    <div v-if="store.loadError" class="error">
      <p>{{ store.loadError }}</p>
      <button class="btn" type="button" @click="loadQuestion">Retry</button>
    </div>
    <p v-else-if="!store.question" class="message">Loading&hellip;</p>
    <template v-else>
      <div class="question-row">
        <h2 class="question">
          <span
            v-for="(word, i) in speech.words"
            :key="i"
            :class="['word', { lit: speech.highlightIndex === i }]"
            >{{ word.text }}{{ word.trail }}</span
          >
        </h2>
        <button class="btn read-btn" type="button" @click="toggleReadAloud">
          {{ speech.speaking ? "Stop" : "Read aloud" }}
        </button>
      </div>
      <p v-if="speech.unavailable" class="speech-note">
        Read-aloud is not available in this browser. You can still answer the
        question.
      </p>
      <div class="answers">
        <AnswerCard
          v-for="(option, index) in store.question.options"
          :key="index"
          :index="index"
          :option="option"
          :disabled="done"
        />
      </div>
      <HintStack />
      <button
        class="btn"
        type="button"
        :disabled="!hasAnswer || store.submitting || done"
        @click="submitAnswer"
      >
        Check answer
      </button>
      <button
        class="btn hint-btn"
        type="button"
        :disabled="store.hintSteps.length >= 3 || done || store.hintPending"
        @click="requestHint"
      >
        Hint
      </button>
      <button
        class="btn break-btn"
        type="button"
        @click="store.breakActive = true"
      >
        Take a break
      </button>
      <p v-if="solved" class="message">Nice work.</p>
      <p v-if="store.verdict?.capped" class="message">
        Done for today. Come back tomorrow.
      </p>
      <p v-else-if="revealed" class="message">
        Now you know how it works. Try the next one.
      </p>
      <p v-else-if="store.verdict" class="message">Not quite. Try again.</p>
      <button v-if="done" class="btn" type="button" @click="nextQuestion">
        Next
      </button>
    </template>
  </section>
</template>

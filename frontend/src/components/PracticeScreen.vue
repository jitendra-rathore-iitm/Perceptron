<script setup>
import { computed } from "vue";
import AnswerCard from "./AnswerCard.vue";
import { loadQuestion, nextQuestion, store, submitAnswer } from "../store";

const cardClass = computed(() => {
  if (!store.verdict || typeof store.verdict !== "object") return "";
  return store.verdict.correct ? "is-right" : "is-wrong";
});
const hasAnswer = computed(() => store.selected !== null);
const solved = computed(() => store.verdict?.correct === true);
</script>

<template>
  <section class="card" :class="cardClass">
    <div v-if="store.loadError" class="error">
      <p>{{ store.loadError }}</p>
      <button class="btn" type="button" @click="loadQuestion">Retry</button>
    </div>
    <p v-else-if="!store.question" class="message">Loading&hellip;</p>
    <template v-else>
      <h2 class="question">{{ store.question.text }}</h2>
      <div class="answers">
        <AnswerCard
          v-for="(option, index) in store.question.options"
          :key="index"
          :index="index"
          :option="option"
        />
      </div>
      <button
        class="btn"
        type="button"
        :disabled="!hasAnswer || store.submitting || solved"
        @click="submitAnswer"
      >
        Check answer
      </button>
      <p v-if="store.verdict?.correct" class="message">Nice work.</p>
      <p v-else-if="store.verdict" class="message">Not quite. Try again.</p>
      <button v-if="solved" class="btn" type="button" @click="nextQuestion">
        Next
      </button>
    </template>
  </section>
</template>

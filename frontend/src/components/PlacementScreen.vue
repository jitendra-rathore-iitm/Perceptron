<script setup>
import { computed } from "vue";
import AnswerCard from "./AnswerCard.vue";
import { enterPractice, startPlacement, store, submitPlacement } from "../store";

const question = computed(
  () => store.placementQuestions[store.placementIndex],
);
const progress = computed(() => store.placementIndex + 1);
const hasAnswer = computed(() => store.selected !== null);

function check() {
  if (!hasAnswer.value || store.placementBusy) return;
  submitPlacement(store.selected);
}

function skip() {
  submitPlacement(null);
}
</script>

<template>
  <section class="card" :key="question?.id ?? 'placement-empty'">
    <template v-if="store.placementResult !== null">
      <h2 class="question">You're starting at Level {{ store.placementResult }}.</h2>
      <p class="message">Questions will match that level. You can always practise.</p>
      <button class="btn start-btn" type="button" @click="enterPractice">
        Start practising
      </button>
    </template>
    <template v-else-if="!question">
      <p v-if="store.loadError" class="error">
        {{ store.loadError }}
        <button class="btn" type="button" @click="startPlacement">Retry</button>
      </p>
      <p v-else class="message">Loading&hellip;</p>
    </template>
    <template v-else>
      <p class="progress">Question {{ progress }} of 6</p>
      <h2 class="question">{{ question.text }}</h2>
      <div class="answers">
        <AnswerCard
          v-for="(option, index) in question.options"
          :key="index"
          :index="index"
          :option="option"
        />
      </div>
      <p v-if="store.loadError" class="error">{{ store.loadError }}</p>
      <button
        class="btn start-btn"
        type="button"
        :disabled="!hasAnswer || store.placementBusy"
        @click="check"
      >
        Check answer
      </button>
      <button
        class="btn"
        type="button"
        :disabled="store.placementBusy"
        @click="skip"
      >
        Skip
      </button>
    </template>
  </section>
</template>

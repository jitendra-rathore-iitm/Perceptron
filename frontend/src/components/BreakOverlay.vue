<script setup>
import { onBeforeUnmount, onMounted, ref } from "vue";
import { store } from "../store";

const phase = ref("Breathe in.");
let timer = null;

onMounted(() => {
  timer = setInterval(() => {
    phase.value = phase.value === "Breathe in." ? "Breathe out." : "Breathe in.";
  }, 4000);
});

onBeforeUnmount(() => {
  clearInterval(timer);
});

function keepGoing() {
  store.breakActive = false;
}
</script>

<template>
  <div class="break-overlay" role="dialog" aria-label="Take a break">
    <div class="break-card">
      <div class="breath-circle" aria-hidden="true"></div>
      <p class="breath-text">{{ phase }}</p>
      <p class="breath-note">Your question and honey are safe.</p>
      <button class="btn" type="button" @click="keepGoing">Keep going</button>
    </div>
  </div>
</template>

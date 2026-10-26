<script setup>
import { computed } from "vue";
import { enterPractice, restoreSession, startOver, startPlacement, store } from "../store";

const returning = computed(() => !store.isNew);

function primary() {
  if (returning.value) {
    if (store.level === null) {
      startPlacement();
    } else {
      enterPractice();
    }
  } else {
    startPlacement();
  }
}
</script>

<template>
  <section class="card welcome">
    <h1 class="welcome-title">Perceptron</h1>
    <p class="welcome-line">Maths that goes at your pace.</p>
    <p v-if="returning" class="welcome-line">Welcome back.</p>
    <p class="device-note">
      Your honey and progress live in this browser on this device. No signup,
      no accounts.
    </p>
    <div class="welcome-actions">
      <button class="btn start-btn" type="button" @click="primary">
        {{ returning ? "Continue" : "Start" }}
      </button>
      <button
        v-if="returning"
        class="btn"
        type="button"
        @click="startOver"
      >
        Start over
      </button>
    </div>
    <p v-if="store.loadError" class="error">
      {{ store.loadError }}
      <button class="btn" type="button" @click="restoreSession">Retry</button>
    </p>
  </section>
</template>

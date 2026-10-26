<script setup>
import { ref, watch } from "vue";
import { store } from "../store";

const bump = ref(false);

watch(
  () => store.honeyTotal,
  () => {
    bump.value = false;
    requestAnimationFrame(() => {
      bump.value = true;
      setTimeout(() => {
        bump.value = false;
      }, 450);
    });
  },
);
</script>

<template>
  <nav class="navbar">
    <span class="logo">Perceptron</span>
    <span :class="['honey', { bump }]">Honey: {{ store.honeyTotal }}</span>
    <button
      class="panel-btn"
      type="button"
      title="Dyslexia panel"
      aria-label="Dyslexia panel"
    >
      Dyslexia
    </button>
  </nav>
</template>

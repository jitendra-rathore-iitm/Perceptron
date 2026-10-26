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
    <span :class="['honey', { bump }]">{{ store.honeyTotal }} drops</span>
    <button class="panel-btn" type="button" title="Dyslexia panel">aA</button>
  </nav>
</template>

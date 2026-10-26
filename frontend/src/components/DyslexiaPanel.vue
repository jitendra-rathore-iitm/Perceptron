<script setup>
import { computed } from "vue";
import { store, toggleDyslexia } from "../store";

const mode = computed(() => (store.dyslexia ? "On" : "Off"));
</script>

<template>
  <div class="panel" role="dialog" aria-label="Dyslexia panel">
    <p class="panel-title">Dyslexia-friendly mode</p>
    <p class="panel-state">Currently: <strong>{{ mode }}</strong></p>
    <button
      class="btn"
      :class="{ 'toggle-on': store.dyslexia }"
      type="button"
      :aria-pressed="store.dyslexia"
      @click="toggleDyslexia"
    >
      {{ store.dyslexia ? "Switch to ordinary mode" : "Switch to dyslexia-friendly mode" }}
    </button>
    <p class="panel-note">Changes font, spacing, text size and motion everywhere, right away.</p>
  </div>
</template>

<script setup>
import { store } from "../store";
</script>

<template>
  <nav class="navbar">
    <span class="logo">Perceptron</span>
    <span class="honey">{{ store.honeyTotal }} drops</span>
    <button class="panel-btn" type="button" title="Dyslexia panel">aA</button>
  </nav>
</template>

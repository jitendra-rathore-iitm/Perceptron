<script setup>
import { onMounted } from "vue";
import NavBar from "./components/NavBar.vue";
import PracticeScreen from "./components/PracticeScreen.vue";
import { loadQuestion, store } from "./store";

onMounted(() => {
  loadQuestion();
});
</script>

<template>
  <NavBar />
  <main class="page">
    <PracticeScreen v-if="store.screen === 'practice'" />
  </main>
  <footer class="footer">Made with love by Jitendra</footer>
</template>

<script setup>
import { onMounted } from "vue";
import NavBar from "./components/NavBar.vue";
import PracticeScreen from "./components/PracticeScreen.vue";
import { loadQuestion, restoreSession, store } from "./store";

onMounted(async () => {
  await restoreSession();
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

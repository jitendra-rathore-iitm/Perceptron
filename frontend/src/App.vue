<script setup>
import { onMounted } from "vue";
import NavBar from "./components/NavBar.vue";
import PlacementScreen from "./components/PlacementScreen.vue";
import PracticeScreen from "./components/PracticeScreen.vue";
import WelcomeScreen from "./components/WelcomeScreen.vue";
import { restoreSession, store } from "./store";

onMounted(() => {
  restoreSession();
});
</script>

<template>
  <NavBar />
  <main class="page">
    <WelcomeScreen v-if="store.screen === 'welcome'" />
    <PlacementScreen v-else-if="store.screen === 'placement'" />
    <PracticeScreen v-else />
  </main>
  <footer class="footer">Made with love by Jitendra</footer>
</template>

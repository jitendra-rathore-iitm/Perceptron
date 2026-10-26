import { createApp, watch } from "vue";
import App from "./App.vue";
import { store } from "./store";
import "./styles/base.css";

watch(
  () => store.dyslexia,
  (on) => {
    document.documentElement.toggleAttribute("data-dyslexia", on);
  },
  { immediate: true },
);

createApp(App).mount("#app");

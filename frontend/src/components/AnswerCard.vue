<script setup>
import { store } from "../store";

defineProps({
  index: {
    type: Number,
    required: true,
  },
  option: {
    type: String,
    required: true,
  },
});
</script>

<template>
  <button
    type="button"
    class="answer"
    :class="{ selected: store.selected === index }"
    @click="store.selected = index"
  >
    {{ option }}
  </button>
</template>

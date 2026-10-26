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
  disabled: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <button
    type="button"
    class="answer"
    :class="{ selected: store.selected === index }"
    :disabled="disabled"
    @click="store.selected = index"
  >
    {{ option }}
  </button>
</template>

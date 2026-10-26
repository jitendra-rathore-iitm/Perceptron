<script setup>
import { store } from "../store";
</script>

<template>
  <div v-if="store.hintSteps.length || store.revealed" class="hints">
    <div
      v-for="(hint, i) in store.hintSteps"
      :key="i"
      :class="['hint', hint.kind]"
    >
      <p>{{ hint.text }}</p>
    </div>
    <div v-if="store.revealed" class="hint reveal">
      <p>
        The correct answer is <strong>{{ store.revealed.correctOption }}</strong
        >.
      </p>
      <p>{{ store.revealed.explanation }}</p>
      <p class="hint-note">
        No honey for this one. The same skill will come back in a fresh
        question.
      </p>
    </div>
  </div>
</template>

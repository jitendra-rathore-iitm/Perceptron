import { reactive } from "vue";
import { checkAnswer, getPracticeQuestion } from "./api";

const DEVICE_ID_KEY = "perceptron_device_id";

function loadDeviceId() {
  let id = localStorage.getItem(DEVICE_ID_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(DEVICE_ID_KEY, id);
  }
  return id;
}

export const store = reactive({
  deviceId: loadDeviceId(),
  screen: "practice",
  question: null,
  selected: null,
  verdict: null,
  submitting: false,
  honeyTotal: 0,
  honeyToday: 0,
  loadError: null,
});

export async function loadQuestion() {
  store.selected = null;
  store.verdict = null;
  store.question = null;
  try {
    store.question = await getPracticeQuestion(store.deviceId);
    store.loadError = null;
  } catch (error) {
    store.loadError = error.message;
  }
}

export async function submitAnswer() {
  if (store.selected === null || store.submitting) {
    return;
  }
  store.submitting = true;
  try {
    const result = await checkAnswer(
      store.deviceId,
      store.question.id,
      store.selected,
    );
    store.verdict = result;
    if (result.correct) {
      store.honeyTotal = result.totalHoney;
      store.honeyToday = result.honeyToday;
    }
  } catch (error) {
    store.loadError = error.message;
    store.verdict = null;
  } finally {
    store.submitting = false;
  }
}

export function nextQuestion() {
  loadQuestion();
}

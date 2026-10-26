import { reactive } from "vue";
import { checkAnswer, getPracticeQuestion, revealHint, startSession } from "./api";
import { setQuestionText, stopSpeech } from "./speech";

const DEVICE_ID_KEY = "perceptron_device_id";

function loadDeviceId() {
  let id = localStorage.getItem(DEVICE_ID_KEY);
  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem(DEVICE_ID_KEY, id);
  }
  return id;
}

function localDate() {
  const now = new Date();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${now.getFullYear()}-${month}-${day}`;
}

export const store = reactive({
  deviceId: loadDeviceId(),
  screen: "practice",
  question: null,
  selected: null,
  verdict: null,
  submitting: false,
  hintSteps: [],
  hintPending: false,
  revealed: null,
  honeyTotal: 0,
  honeyToday: 0,
  level: null,
  dyslexia: false,
  loadError: null,
});

export async function restoreSession() {
  try {
    const session = await startSession(store.deviceId, localDate());
    store.honeyTotal = session.totalHoney;
    store.honeyToday = session.honeyToday;
    store.level = session.level;
    store.dyslexia = session.dyslexia;
    store.loadError = null;
  } catch (error) {
    store.loadError = error.message;
  }
}

export async function loadQuestion() {
  stopSpeech();
  store.selected = null;
  store.verdict = null;
  store.hintSteps = [];
  store.revealed = null;
  store.question = null;
  try {
    store.question = await getPracticeQuestion(store.deviceId);
    store.loadError = null;
    setQuestionText(store.question.text);
  } catch (error) {
    store.loadError = error.message;
  }
}

export async function submitAnswer() {
  if (store.selected === null || store.submitting) {
    return;
  }
  stopSpeech();
  store.submitting = true;
  try {
    const result = await checkAnswer(
      store.deviceId,
      store.question.id,
      store.selected,
    );
    store.verdict = result;
    if (result.hint) {
      store.hintSteps.push(result.hint);
    }
    if (result.revealed) {
      store.revealed = result;
    }
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

export async function requestHint() {
  if (store.hintPending || store.hintSteps.length >= 3 || store.revealed) {
    return;
  }
  store.hintPending = true;
  try {
    const result = await revealHint(store.deviceId, store.question.id);
    if (result.hint) {
      store.hintSteps.push(result.hint);
    }
  } catch (error) {
    store.loadError = error.message;
  } finally {
    store.hintPending = false;
  }
}

export function nextQuestion() {
  loadQuestion();
}

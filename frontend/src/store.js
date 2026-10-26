import { reactive } from "vue";
import {
  checkAnswer,
  getPlacementQuestions,
  getPracticeQuestion,
  resetProgress,
  revealHint,
  startSession,
  submitPlacementAnswer,
} from "./api";
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
  screen: "welcome",
  isNew: true,
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
  placementQuestions: [],
  placementRows: [],
  placementIndex: 0,
  placementBusy: false,
  placementResult: null,
  loadError: null,
});

export async function restoreSession() {
  try {
    const session = await startSession(store.deviceId, localDate());
    store.isNew = session.isNew;
    store.honeyTotal = session.totalHoney;
    store.honeyToday = session.honeyToday;
    store.level = session.level;
    store.dyslexia = session.dyslexia;
    store.placementRows = session.placement;
    store.screen = "welcome";
    store.loadError = null;
  } catch (error) {
    store.loadError = error.message;
  }
}

export async function enterPractice() {
  store.screen = "practice";
  store.placementResult = null;
  loadQuestion();
}

export async function startPlacement() {
  stopSpeech();
  try {
    const result = await getPlacementQuestions(store.deviceId);
    store.placementQuestions = result.questions;
    store.placementIndex = Math.min(
      (store.placementRows ?? []).length,
      result.questions.length,
    );
    store.selected = null;
    store.placementResult = null;
    store.screen = "placement";
    store.loadError = null;
  } catch (error) {
    store.loadError = error.message;
  }
}

export async function submitPlacement(selected) {
  if (store.placementBusy) return;
  const question = store.placementQuestions[store.placementIndex];
  if (!question) return;
  store.placementBusy = true;
  try {
    const result = await submitPlacementAnswer(
      store.deviceId,
      question.id,
      selected,
    );
    if (result.done) {
      store.level = result.placedLevel;
      store.placementResult = result.placedLevel;
      store.placementRows = [];
    } else {
      store.placementIndex += 1;
      store.selected = null;
    }
    store.loadError = null;
  } catch (error) {
    store.loadError = error.message;
  } finally {
    store.placementBusy = false;
  }
}

export async function startOver() {
  try {
    await resetProgress(store.deviceId);
    store.honeyTotal = 0;
    store.honeyToday = 0;
    store.level = null;
    store.isNew = true;
    store.placementRows = [];
    store.placementQuestions = [];
    store.selected = null;
    store.verdict = null;
    store.hintSteps = [];
    store.revealed = null;
    store.screen = "welcome";
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

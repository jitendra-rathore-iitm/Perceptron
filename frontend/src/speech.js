import { reactive } from "vue";

export const speech = reactive({
  supported: typeof window !== "undefined" && "speechSynthesis" in window,
  words: [],
  highlightIndex: null,
  speaking: false,
  unavailable: false,
});

let stopped = true;

function wordList(text) {
  const words = [];
  for (const match of text.matchAll(/\S+/g)) {
    words.push({ text: match[0], trail: " ", start: match.index });
  }
  if (words.length > 0) {
    words[words.length - 1].trail = "";
  }
  return words;
}

function finish() {
  speech.speaking = false;
  speech.highlightIndex = null;
}

export function setQuestionText(text) {
  stopped = true;
  speech.speaking = false;
  speech.unavailable = false;
  speech.words = wordList(text);
  speech.highlightIndex = null;
}

export function stopSpeech() {
  stopped = true;
  speech.speaking = false;
  speech.highlightIndex = null;
  if (speech.supported) {
    window.speechSynthesis.cancel();
  }
}

function speakEachWord() {
  stopped = false;
  speech.speaking = true;
  let index = 0;
  const speakNext = () => {
    if (stopped || index >= speech.words.length) {
      finish();
      return;
    }
    speech.highlightIndex = index;
    const utterance = new SpeechSynthesisUtterance(speech.words[index].text);
    utterance.onend = () => {
      if (stopped) return;
      index += 1;
      speakNext();
    };
    utterance.onerror = () => {
      if (stopped) return;
      if (index === 0) {
        speech.unavailable = true;
        finish();
        return;
      }
      index += 1;
      speakNext();
    };
    window.speechSynthesis.speak(utterance);
  };
  speakNext();
}

export function speakQuestion(text) {
  stopSpeech();
  if (!speech.supported) {
    speech.unavailable = true;
    return;
  }
  setQuestionText(text);
  speakEachWord();
}

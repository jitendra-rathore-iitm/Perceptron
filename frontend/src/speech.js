import { reactive } from "vue";

export const speech = reactive({
  supported: typeof window !== "undefined" && "speechSynthesis" in window,
  words: [],
  highlightIndex: null,
  speaking: false,
  unavailable: false,
});

let timer = null;
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

function highlightAt(charIndex) {
  for (let i = speech.words.length - 1; i >= 0; i -= 1) {
    if (speech.words[i].start <= charIndex) {
      speech.highlightIndex = i;
      return;
    }
  }
  speech.highlightIndex = null;
}

function finish() {
  speech.speaking = false;
  speech.highlightIndex = null;
  clearTimeout(timer);
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
  clearTimeout(timer);
  if (speech.supported) {
    window.speechSynthesis.cancel();
  }
}

function speakWordByWord() {
  let index = 0;
  const synth = window.speechSynthesis;
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
    synth.speak(utterance);
  };
  speech.speaking = true;
  speakNext();
}

function speakWhole(text) {
  stopped = false;
  speech.speaking = true;
  speech.highlightIndex = null;
  let sawBoundary = false;
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.onboundary = (event) => {
    sawBoundary = true;
    highlightAt(event.charIndex ?? 0);
  };
  utterance.onend = () => {
    if (!stopped) {
      finish();
    }
  };
  utterance.onerror = () => {
    if (!stopped) {
      finish();
    }
  };
  window.speechSynthesis.speak(utterance);
  timer = setTimeout(() => {
    if (!stopped && speech.speaking && !sawBoundary) {
      window.speechSynthesis.cancel();
      speakWordByWord();
    }
  }, 700);
}

export function speakQuestion(text) {
  stopSpeech();
  if (!speech.supported) {
    speech.unavailable = true;
    return;
  }
  setQuestionText(text);
  speakWhole(text);
}

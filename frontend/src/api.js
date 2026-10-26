const FRIENDLY_MESSAGES = {
  bad_request: "Something went wrong with that request. Refresh the page.",
  invalid_selection: "Pick one of the four answers before checking.",
  unknown_question: "That question is no longer available. A fresh one is loading.",
  unknown_device: "We couldn't find your progress on this device, so you're starting fresh.",
  server_error: "Something went wrong on our side. Try again.",
};

const NETWORK_MESSAGE = "Can't reach the server. Check your connection and try again.";

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error(NETWORK_MESSAGE);
  }
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const code = body?.error?.code;
    throw new Error(
      FRIENDLY_MESSAGES[code] ??
        body?.error?.description ??
        NETWORK_MESSAGE,
    );
  }
  return body;
}

export function startSession(deviceId, today) {
  return request("/api/session", {
    method: "POST",
    body: JSON.stringify({ deviceId, today }),
  });
}

export function getPracticeQuestion(deviceId) {
  return request(
    `/api/practice/question?deviceId=${encodeURIComponent(deviceId)}`,
  );
}

export function checkAnswer(deviceId, questionId, selected) {
  return request("/api/check", {
    method: "POST",
    body: JSON.stringify({ deviceId, questionId, selected }),
  });
}

export function revealHint(deviceId, questionId) {
  return request("/api/hint", {
    method: "POST",
    body: JSON.stringify({ deviceId, questionId }),
  });
}

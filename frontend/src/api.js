async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const description =
      body?.error?.description ??
      "Something went wrong on our side. Try again.";
    throw new Error(description);
  }
  return body;
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

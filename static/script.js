const form = document.getElementById("translate-form");
const textArea = document.getElementById("text");
const sourceSelect = document.getElementById("source_language");
const targetSelect = document.getElementById("target_language");
const swapBtn = document.getElementById("swap-btn");
const translateBtn = document.getElementById("translate-btn");
const charCount = document.getElementById("char-count");
const resultWrap = document.getElementById("result-wrap");
const resultBubble = document.getElementById("result-bubble");
const resultText = document.getElementById("result-text");
const copyBtn = document.getElementById("copy-btn");

function updateCharCount() {
  const n = textArea.value.length;
  charCount.textContent = `${n} character${n === 1 ? "" : "s"}`;
}
textArea.addEventListener("input", updateCharCount);
updateCharCount();

swapBtn.addEventListener("click", () => {
  const sourceVal = sourceSelect.value;
  const targetVal = targetSelect.value;
  // Only swap if the source language is a concrete choice (not "Detect language")
  if (!sourceVal) return;
  sourceSelect.value = targetVal;
  targetSelect.value = sourceVal;
});

function showResult(text, isError) {
  resultText.textContent = text;
  resultBubble.classList.toggle("error", !!isError);
  resultWrap.classList.add("visible");
}

function setLoading(isLoading) {
  translateBtn.disabled = isLoading;
  translateBtn.classList.toggle("loading", isLoading);
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = textArea.value.trim();
  if (!text) {
    showResult("Enter some text to translate.", true);
    return;
  }

  setLoading(true);
  try {
    const res = await fetch("/api/translate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        source_language: sourceSelect.value,
        target_language: targetSelect.value,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      showResult(data.error || "Something went wrong. Please try again.", true);
    } else {
      showResult(data.translated_text, false);
    }
  } catch (err) {
    showResult("Couldn't reach the server. Please try again.", true);
  } finally {
    setLoading(false);
  }
});

copyBtn.addEventListener("click", async () => {
  const text = resultText.textContent;
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    const original = copyBtn.textContent;
    copyBtn.textContent = "Copied";
    setTimeout(() => { copyBtn.textContent = original; }, 1500);
  } catch (err) {
    // Clipboard API unavailable — silently ignore.
  }
});

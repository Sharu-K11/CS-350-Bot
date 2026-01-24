(() => {
  const messages = document.getElementById("messages");
  const chatForm = document.getElementById("chatForm");
  const prompt = document.getElementById("prompt");
  const clearBtn = document.getElementById("clearBtn");
  const newChatBtn = document.getElementById("newChatBtn");
  const sendBtn = document.getElementById("sendBtn");

  function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
  }

  function addAssistant(text, sources = []) {
    const sec = document.createElement("section");
    sec.className = "turn turn-assistant";

    const sourcesHtml = sources.length
      ? `<div class="turn-foot">
          ${sources.map(s => `<span class="badge bg-secondary-subtle border text-body me-1">${escapeHtml(s)}</span>`).join("")}
        </div>`
      : "";

    sec.innerHTML = `
      <div class="turn-inner">
        <div class="turn-head"><div class="role">Assistant</div></div>
        <div class="turn-body"></div>
        ${sourcesHtml}
      </div>
    `;
    sec.querySelector(".turn-body").textContent = text;
    messages.appendChild(sec);
    scrollToBottom();
  }

  function addUser(text) {
    const sec = document.createElement("section");
    sec.className = "turn turn-user";
    sec.innerHTML = `
      <div class="turn-inner">
        <div class="turn-head justify-content-end"><div class="role">You</div></div>
        <div class="turn-body user-bubble-wrap">
          <div class="user-bubble"></div>
        </div>
      </div>
    `;
    sec.querySelector(".user-bubble").textContent = text;
    messages.appendChild(sec);
    scrollToBottom();
  }

  function addThinking() {
    const sec = document.createElement("section");
    sec.className = "turn turn-assistant";
    sec.id = "thinkingTurn";
    sec.innerHTML = `
      <div class="turn-inner">
        <div class="turn-head"><div class="role">Assistant</div></div>
        <div class="turn-body">Thinking…</div>
      </div>
    `;
    messages.appendChild(sec);
    scrollToBottom();
  }

  function removeThinking() {
    const t = document.getElementById("thinkingTurn");
    if (t) t.remove();
  }

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function clearMessages() {
    messages.innerHTML = "";
  }

  clearBtn?.addEventListener("click", clearMessages);
  newChatBtn?.addEventListener("click", () => {
    clearMessages();
    prompt.focus();
  });

  chatForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = prompt.value.trim();
    if (!text) return;

    addUser(text);
    prompt.value = "";
    prompt.focus();

    sendBtn.disabled = true;
    addThinking();

    // Demo (replace with fetch() to Django API)
    setTimeout(() => {
      removeThinking();
      addAssistant(
        "This is a ChatGPT-style UI. Next we’ll connect it to your Django RAG endpoint.",
        ["example.pdf", "page 3"]
      );
      sendBtn.disabled = false;
    }, 500);
  });

  scrollToBottom();
})();

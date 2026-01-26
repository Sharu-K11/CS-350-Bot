(() => {
  const messages = document.getElementById("messages");
  const chatForm = document.getElementById("chatForm");
  const prompt = document.getElementById("prompt");
  const clearBtn = document.getElementById("clearBtn");
  const newChatBtn = document.getElementById("newChatBtn");
  const sendBtn = document.getElementById("sendBtn");

  // Change this to your endpoint
  const API_URL = "/api/ask/";

  function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight;
  }

  function getCookie(name) {
    // Django CSRF cookie helper
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  function escapeHtml(str) {
    return String(str)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function addAssistant(text, sources = []) {
    const sec = document.createElement("section");
    sec.className = "turn turn-assistant";

    const sourcesHtml = sources?.length
      ? `<div class="turn-foot">
          ${sources
        .map(
          (s) =>
            `<span class="badge bg-secondary-subtle border text-body me-1">${escapeHtml(
              s
            )}</span>`
        )
        .join("")}
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

  function clearMessages() {
    messages.innerHTML = "";
  }

  clearBtn?.addEventListener("click", clearMessages);
  newChatBtn?.addEventListener("click", () => {
    clearMessages();
    prompt.focus();
  });

  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = prompt.value.trim();
    if (!text) return;

    addUser(text);
    prompt.value = "";
    prompt.focus();

    sendBtn.disabled = true;
    addThinking();

    try {
      const csrftoken = getCookie("csrftoken");

      const res = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,   // REQUIRED
        },
        body: JSON.stringify({ question: text }),
      });


      const data = await res.json().catch(() => ({}));

      removeThinking();

      if (!res.ok) {
        addAssistant(data.error || `Server error (${res.status})`);
      } else {
        // Support either "answer" or plain string response
        const answer = data.answer ?? String(data);
        const sources = data.sources ?? [];
        addAssistant(answer, sources);
      }
    } catch (err) {
      removeThinking();
      addAssistant("Network error. Check server is running and endpoint is correct.");
      console.error(err);
    } finally {
      sendBtn.disabled = false;
    }
  });

  scrollToBottom();
})();

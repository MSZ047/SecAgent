function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function renderErrorView(mount, message, onReset) {
  mount.innerHTML = `
    <div class="error-shell">
      <div class="error-card">
        <h2 class="error-title">Unable to analyze this URL</h2>
        <p class="error-text">${escapeHtml(message || "发生未知错误。")}</p>

        <div class="error-actions">
          <button id="retryBtn" class="primary-btn" type="button">重新输入 URL</button>
        </div>
      </div>
    </div>
  `;

  const retryBtn = mount.querySelector("#retryBtn");
  retryBtn.addEventListener("click", onReset);
}
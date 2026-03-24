export function renderUrlInput({
  mount,
  onSubmit,
}) {
  mount.innerHTML = `
    <div class="url-input-wrap">
      <form id="urlForm">
        <div class="url-input-card">
          <input
            id="urlInput"
            class="url-input"
            type="text"
            placeholder="输入要分析的 URL 地址..."
            autocomplete="off"
          />
          <button id="analyzeBtn" class="primary-btn" type="submit" disabled>
            <span class="btn-text">开始分析</span>
          </button>
        </div>
        <div id="inputError" class="input-error" style="display:none;"></div>
      </form>
    </div>
  `;

  const form = mount.querySelector("#urlForm");
  const input = mount.querySelector("#urlInput");
  const button = mount.querySelector("#analyzeBtn");
  const errorEl = mount.querySelector("#inputError");

  const setError = (message = "") => {
    if (!message) {
      errorEl.style.display = "none";
      errorEl.textContent = "";
      return;
    }
    errorEl.style.display = "block";
    errorEl.textContent = message;
  };

  const updateButton = () => {
    button.disabled = !input.value.trim();
  };

  input.addEventListener("input", () => {
    setError("");
    updateButton();
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const value = input.value.trim();

    if (!value) {
      setError("请输入 URL。");
      return;
    }

    button.disabled = true;
    await onSubmit(value, setError);
    updateButton();
  });

  input.focus();
}
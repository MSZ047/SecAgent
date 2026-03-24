import { AppStatus, state, subscribe, setState, resetState } from "./state.js";
import { validateUrl, analyzeUrl } from "./api.js";
import { renderUrlInput } from "./components/url-input.js";
import { renderLoadingView } from "./components/loading-view.js";
import { renderResultView } from "./components/result-view.js";
import { renderErrorView } from "./components/error-view.js";

const homeView = document.getElementById("homeView");
const workspaceView = document.getElementById("workspaceView");
const contentMount = document.getElementById("contentMount");
const urlInputMount = document.getElementById("urlInputMount");
const topbar = document.getElementById("topbar");
const urlPill = document.getElementById("urlPill");
const statusBadge = document.getElementById("statusBadge");
const backBtn = document.getElementById("backBtn");

function statusText(status) {
  switch (status) {
    case AppStatus.IDLE:
      return "Idle";
    case AppStatus.VALIDATING:
      return "Validating";
    case AppStatus.LOADING:
      return "Analyzing";
    case AppStatus.RESULT:
      return "Completed";
    case AppStatus.ERROR:
      return "Error";
    default:
      return "Unknown";
  }
}

function syncLayout() {
  const isHome = state.status === AppStatus.IDLE;

  homeView.classList.toggle("hidden", !isHome);
  workspaceView.classList.toggle("hidden", isHome);
  topbar.classList.toggle("hidden", isHome);

  statusBadge.textContent = statusText(state.status);
  urlPill.textContent = state.currentUrl || "-";
}

function renderWorkspace() {
  if (state.status === AppStatus.LOADING || state.status === AppStatus.VALIDATING) {
    renderLoadingView(contentMount);
    return;
  }

  if (state.status === AppStatus.RESULT && state.result) {
    renderResultView(contentMount, state.result);
    return;
  }

  if (state.status === AppStatus.ERROR) {
    renderErrorView(contentMount, state.error || "分析失败。", () => {
      resetState();
      initHome();
    });
    return;
  }

  contentMount.innerHTML = "";
}

async function handleSubmit(inputValue, setInlineError) {
  setState({
    status: AppStatus.VALIDATING,
    error: null,
  });

  syncLayout();
  renderWorkspace();

  const validation = await validateUrl(inputValue);

  if (!validation.ok) {
    setState({
      status: AppStatus.IDLE,
      error: null,
    });
    syncLayout();
    renderWorkspace();
    setInlineError(validation.message || "URL 校验失败");
    return;
  }

  const normalizedUrl = validation.normalized_url;

  setState({
    status: AppStatus.LOADING,
    currentUrl: normalizedUrl,
    result: null,
    error: null,
  });

  syncLayout();
  renderWorkspace();

  const result = await analyzeUrl(normalizedUrl);

  if (result.status === "success") {
    setState({
      status: AppStatus.RESULT,
      result,
      error: null,
    });
  } else {
    setState({
      status: AppStatus.ERROR,
      result: null,
      error: result.message || "分析失败，请稍后重试。",
    });
  }

  syncLayout();
  renderWorkspace();
}

function initHome() {
  renderUrlInput({
    mount: urlInputMount,
    onSubmit: handleSubmit,
  });
}

function renderApp() {
  syncLayout();
  renderWorkspace();
}

backBtn.addEventListener("click", () => {
  resetState();
  initHome();
  renderApp();
});

subscribe(() => {
  renderApp();
});

initHome();
renderApp();
export const AppStatus = {
  IDLE: "IDLE",
  VALIDATING: "VALIDATING",
  LOADING: "LOADING",
  RESULT: "RESULT",
  ERROR: "ERROR",
};

export const state = {
  status: AppStatus.IDLE,
  currentUrl: "",
  result: null,
  error: null,
};

const listeners = new Set();

export function subscribe(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function setState(patch) {
  Object.assign(state, patch);
  listeners.forEach((listener) => listener(state));
}

export function resetState() {
  state.status = AppStatus.IDLE;
  state.currentUrl = "";
  state.result = null;
  state.error = null;
  listeners.forEach((listener) => listener(state));
}
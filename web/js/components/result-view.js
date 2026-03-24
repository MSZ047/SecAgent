function renderList(items = []) {
  return items
    .map((item) => `
      <div class="list-item">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="list-item-icon">
          <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>${escapeHtml(item)}</span>
      </div>
    `)
    .join("");
}

function renderSections(sections = []) {
  return sections
    .map(
      (section) => `
        <div class="section-item">
          <div class="section-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M3 9h18M9 21V9" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>
          <div class="section-content">
            <h4 class="section-name">${escapeHtml(section.name)}</h4>
            <p class="section-desc">${escapeHtml(section.description)}</p>
          </div>
        </div>
      `
    )
    .join("");
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export function renderResultView(mount, result) {
  const domain = result?.meta?.domain ?? "-";
  const path = result?.meta?.path ?? "-";
  const capturedAt = result?.meta?.captured_at ?? "-";

  mount.innerHTML = `
    <div class="result-shell">
      <section class="page-head">
        <div class="page-head-content">
          <div class="page-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L4 6v6c0 5.55 3.4 10.74 8 12 4.6-1.26 8-6.45 8-12V6l-8-4z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <div>
            <h1 class="page-title">${escapeHtml(result.title || "Analysis Result")}</h1>
            <p class="page-subtitle">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:14px;height:14px;display:inline-block;vertical-align:middle;margin-right:4px;opacity:0.6">
                <path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              ${escapeHtml(result.url || "-")}
            </p>
          </div>
        </div>

        <div class="meta-row">
          <span class="meta-chip">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:14px;height:14px">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
              <path d="M2 12h20M12 2c-2 2-2 18 0 20" stroke="currentColor" stroke-width="1.5"/>
            </svg>
            ${escapeHtml(domain)}
          </span>
          <span class="meta-chip">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:14px;height:14px">
              <path d="M16 18l6-6-6-6M8 6l-6 6 6 6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            ${escapeHtml(path)}
          </span>
          <span class="meta-chip">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="width:14px;height:14px">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
              <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            ${escapeHtml(capturedAt)}
          </span>
        </div>
      </section>

      <div class="grid">
        <section class="card">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M14 2v6h6M16 13H8M16 17H8M10 9H8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </div>
            <h3 class="card-title">概览</h3>
          </div>
          <p class="card-text">${escapeHtml(result.summary || "")}</p>
        </section>

        <section class="card">
          <div class="card-header">
            <div class="card-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="1.5"/>
              </svg>
            </div>
            <h3 class="card-title">建议</h3>
          </div>
          <div class="list">
            ${renderList(result.recommendations || [])}
          </div>
        </section>
      </div>

      <section class="card">
        <div class="card-header">
          <div class="card-icon warning">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2L2 22h20L12 2z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
              <path d="M12 9v4M12 17v.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h3 class="card-title">关键发现</h3>
        </div>
        <div class="list">
          ${renderList(result.findings || [])}
        </div>
      </section>

      <section class="card">
        <div class="card-header">
          <div class="card-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="1.5"/>
              <path d="M3 9h18M9 21V9" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>
          <h3 class="card-title">页面结构</h3>
        </div>
        <div class="sections-list">
          ${renderSections(result.sections || [])}
        </div>
      </section>
    </div>
  `;
}
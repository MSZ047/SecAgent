export function renderLoadingView(mount) {
  mount.innerHTML = `
    <div class="loading-shell">
      <div class="loading-card">
        <div class="loading-logo">
          <svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="loadingGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#06b6d4"/>
                <stop offset="100%" stop-color="#8b5cf6"/>
              </linearGradient>
            </defs>
            <path d="M24 4L6 12v12c0 11.04 7.68 22.44 18 26 10.32-3.56 18-14.96 18-26V12L24 4z" fill="url(#loadingGrad)" opacity="0.3"/>
            <circle cx="24" cy="22" r="4" fill="url(#loadingGrad)">
              <animate attributeName="r" values="4;8;4" dur="1.5s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="1;0.5;1" dur="1.5s" repeatCount="indefinite"/>
            </circle>
          </svg>
        </div>

        <h2 class="loading-title">
          <span class="loading-text-gradient">AI 正在分析</span>
        </h2>
        <p class="loading-text">
          智能检测页面安全风险，请稍候...
        </p>

        <div class="loading-steps">
          <div class="loading-step">
            <span class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 12a9 9 0 11-9-9" stroke="currentColor" stroke-width="2" stroke-linecap="round">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="2s" repeatCount="indefinite"/>
                </path>
              </svg>
            </span>
            <span>正在获取页面内容</span>
          </div>
          <div class="loading-step">
            <span class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                <path d="M12 2v4M12 18v4M2 12h4M18 12h4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round">
                  <animateTransform attributeName="transform" type="rotate" from="0 12 12" to="360 12 12" dur="3s" repeatCount="indefinite"/>
                </path>
              </svg>
            </span>
            <span>正在解析页面结构</span>
          </div>
          <div class="loading-step">
            <span class="step-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L4 6v6c0 5.55 3.4 10.74 8 12 4.6-1.26 8-6.45 8-12V6l-8-4z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
                <path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </span>
            <span>正在生成分析报告</span>
          </div>
        </div>
      </div>
    </div>
  `;
}
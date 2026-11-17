// Shared MythosHUD Widget Logic

function setGauge(circleElement, percent) {
  if (!circleElement) return;
  const circumference = 220; // 2 * pi * r (r=35)
  const offset = circumference - (percent / 100) * circumference;
  circleElement.style.strokeDashoffset = offset;
}

function updateTheme(themeName) {
  document.body.className = `theme-${themeName.replace('_', '-')}`;
}

window.addEventListener('pywebviewready', function() {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.get_config().then(cfg => {
      if (cfg && cfg.theme) {
        updateTheme(cfg.theme);
      }
    });
  }
});

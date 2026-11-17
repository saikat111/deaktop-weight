// Shared MythosHUD Widget Logic & Utilities

function setGauge(circleElement, percent) {
  if (!circleElement) return;
  const circumference = 220; // 2 * pi * r (r=35)
  const offset = circumference - (Math.min(100, Math.max(0, percent)) / 100) * circumference;
  circleElement.style.strokeDashoffset = offset;
}

function updateTheme(themeName) {
  if (!themeName) return;
  document.body.className = `theme-${themeName.replace(/_/g, '-')}`;
}

function showNotification(title, msg, type = 'warn') {
  let banner = document.getElementById('notification-banner');
  if (!banner) return;
  banner.className = `notification-banner active ${type}`;
  banner.innerHTML = `<strong>${title}:</strong> <span>${msg}</span>`;
  setTimeout(() => {
    banner.className = 'notification-banner';
  }, 5000);
}

function launchApp(appName) {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.launch_app(appName);
  }
}

function openUrl(url) {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.open_url(url);
  }
}

function triggerMedia(action) {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.media_control(action);
  }
}

function triggerWallpaper(themeName) {
  if (window.pywebview && window.pywebview.api) {
    window.pywebview.api.set_wallpaper(themeName);
  }
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

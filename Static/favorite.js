// static/js/favorite.js

// helper برای گرفتن cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(c => {
        const [k, v] = c.trim().split('=');
        if (k === name) cookieValue = decodeURIComponent(v);
      });
    }
    return cookieValue;
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const cfg = document.getElementById('search-config');
    const toggleUrl = cfg.dataset.toggleUrl;         // از تمپلیت می‌گیری
    const csrftoken = getCookie('csrftoken');        // کوکی CSRF
  
    document.querySelectorAll('.favorite-btn').forEach(btn => {
      btn.addEventListener('click', e => {
        e.preventDefault();
        const wordId = btn.dataset.wordId;
  
        fetch(toggleUrl, {
          method: 'POST',
          credentials: 'same-origin',               // بسیار مهم
          headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ word_id: wordId })
        })
        .then(res => {
          if (!res.ok) {
            return res.json().then(err => Promise.reject(err));
          }
          return res.json();
        })
        .then(data => {
          if (data.action === 'added') {
            btn.textContent = '❤️';
            btn.setAttribute('aria-pressed', 'true');
          } else {
            btn.textContent = '🤍';
            btn.setAttribute('aria-pressed', 'false');
          }
        })
        .catch(err => {
          console.error('toggle-favorite error:', err);
        });
      });
    });
  });
  
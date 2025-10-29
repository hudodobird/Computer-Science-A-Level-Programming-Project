// Progress toggling for Example / Question steps

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function toggleCompletion(btn, slug) {
  const step = btn.dataset.step;
  const completed = btn.getAttribute('aria-pressed') === 'true' ? false : true;
  const csrftoken = getCookie('csrftoken');
  try {
    const res = await fetch(`/tutorial/api/progress/${slug}/${step}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken || '',
      },
      body: JSON.stringify({ completed }),
      credentials: 'same-origin',
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const now = !!data.completed;
    btn.setAttribute('aria-pressed', now ? 'true' : 'false');
    btn.textContent = now ? 'Completed' : 'Mark complete';
  } catch (err) {
    console.error('Failed to update progress', err);
    alert('Could not save progress. Are you logged in?');
  }
}

function initProgress() {
  const slug = document.querySelector('.section-layout')?.dataset?.slug || window.location.pathname.split('/').filter(Boolean).pop();
  document.querySelectorAll('.complete-btn[data-step]').forEach(btn => {
    btn.addEventListener('click', () => toggleCompletion(btn, slug));
  });
}

document.addEventListener('DOMContentLoaded', initProgress);

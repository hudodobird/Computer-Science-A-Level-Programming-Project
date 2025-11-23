// Progress toggling for Past Paper Questions

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

async function toggleQuestionCompletion(btn, pk) {
  const completed = btn.getAttribute('aria-pressed') === 'true' ? false : true;
  const csrftoken = getCookie('csrftoken');
  try {
    const res = await fetch(`/pastpapers/api/completion/${pk}/`, {
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
    btn.textContent = now ? 'Completed' : 'Mark as Done';
    btn.classList.toggle('completed', now);
  } catch (err) {
    console.error('Failed to update progress', err);
    alert('Could not save progress. Are you logged in?');
  }
}

function initProgress() {
  const btn = document.getElementById('markDoneBtn');
  if (btn) {
    const pk = btn.dataset.pk;
    btn.addEventListener('click', () => toggleQuestionCompletion(btn, pk));
  }
}

document.addEventListener('DOMContentLoaded', initProgress);

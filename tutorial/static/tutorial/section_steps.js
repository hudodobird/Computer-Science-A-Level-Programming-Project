// Handles two-step UI (Example <-> Question) on tutorial section pages

function decodeEscaped(str) {
  if (!str) return str;
  try {
    // Decode \uXXXX sequences and common escapes
    return str
      .replace(/\\u([0-9a-fA-F]{4})/g, (_, h) => String.fromCharCode(parseInt(h, 16)))
      .replace(/\\n/g, "\n")
      .replace(/\\t/g, "\t");
  } catch (_) {
    return str;
  }
}

function initSectionSteps() {
  document.querySelectorAll('.section-layout').forEach(section => {
    const examplePanel = section.querySelector('.panel--example');
    const questionPanel = section.querySelector('.panel--question');
    const textarea = section.querySelector('.py-runner .code');
    const exampleCode = section.dataset.exampleCode || '';
    const questionCode = section.dataset.questionCode || '';
    const showAnswerBtn = section.querySelector('.show-answer-btn');
    const answerCode = section.querySelector('.answer-code');

    // Don't override initial textarea content rendered by the server.
    // We only swap contents when the user clicks a step. This avoids showing
    // escaped sequences like \u0027 from data attributes.

    const container = section.parentElement; // main > (steps + section)
    const steps = container.querySelectorAll('.steps .step');

    steps.forEach(btn => {
      btn.addEventListener('click', () => {
        steps.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const which = btn.dataset.step;
        if (which === 'example') {
          examplePanel.classList.remove('hidden');
          questionPanel.classList.add('hidden');
          if (exampleCode) textarea.value = decodeEscaped(exampleCode);
        } else {
          examplePanel.classList.add('hidden');
          questionPanel.classList.remove('hidden');
          if (questionCode) textarea.value = decodeEscaped(questionCode);
          // When switching to question, keep answer hidden by default
          if (answerCode && showAnswerBtn) {
            answerCode.classList.add('hidden');
            answerCode.setAttribute('aria-hidden', 'true');
            showAnswerBtn.setAttribute('aria-expanded', 'false');
            showAnswerBtn.textContent = 'Show Answer';
          }
        }
      });
    });

    // Toggle answer visibility
    if (showAnswerBtn && answerCode) {
      showAnswerBtn.addEventListener('click', () => {
        const isHidden = answerCode.classList.contains('hidden');
        answerCode.classList.toggle('hidden');
        answerCode.setAttribute('aria-hidden', isHidden ? 'false' : 'true');
        showAnswerBtn.setAttribute('aria-expanded', isHidden ? 'true' : 'false');
        showAnswerBtn.textContent = isHidden ? 'Hide Answer' : 'Show Answer';
      });
    }
  });
}

document.addEventListener('DOMContentLoaded', initSectionSteps);

// Lightweight Python runner using Pyodide (runs in the browser)
// This file is an ES module because it imports Pyodide from a CDN.

import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.mjs";

let pyodidePromise = null;

async function ensurePyodide(statusEl) {
  if (!pyodidePromise) {
    if (statusEl) statusEl.textContent = "Loading Python runtime (Pyodide)...";
    pyodidePromise = loadPyodide();
    try {
      const pyodide = await pyodidePromise;
        // Use prompt to obtain an input from the user
      const patchInput = `
import builtins
try:
    from js import prompt as _prompt
    def _input(msg=None):
        s = _prompt(msg if msg else "")
        if s is None:
            raise KeyboardInterrupt("Input cancelled")
        return s
    builtins.input = _input
except Exception:
    pass
`;
      await pyodide.runPythonAsync(patchInput);
      if (statusEl) statusEl.textContent = "Ready.";
      return pyodide;
    } catch (e) {
      if (statusEl) statusEl.textContent = "Failed to load Pyodide.";
      throw e;
    }
  }
  return pyodidePromise;
}

async function runPython(code, outputEl, statusEl) {
  const pyodide = await ensurePyodide(statusEl);
  outputEl.textContent = "";
  if (statusEl) statusEl.textContent = "Running...";
  try {
    pyodide.setStdout({ batched: (s) => { outputEl.textContent += s; } });
    pyodide.setStderr({ batched: (s) => { outputEl.textContent += s; } });

    const result = await pyodide.runPythonAsync(code);
    if (typeof result !== "undefined") {
      outputEl.textContent += String(result) + "\n";
    }
    if (statusEl) statusEl.textContent = "Done.";
  } catch (err) {
    outputEl.textContent += `\n${err}\n`;
    if (statusEl) statusEl.textContent = "Error.";
  }
}

function initPyRunner(container) {
  const ta = container.querySelector("textarea");
  const btn = container.querySelector(".run-btn");
  const out = container.querySelector(".output");
  const status = container.querySelector(".status");

  btn.addEventListener("click", () => {
    runPython(ta.value, out, status);
  });
}

function initAll() {
  document.querySelectorAll(".py-runner").forEach(initPyRunner);
}

document.addEventListener("DOMContentLoaded", initAll);

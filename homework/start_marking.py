import sys
import subprocess
from django.utils.safestring import mark_safe

def run_test_cases(submission):
    """
    Runs the submission code against all test cases for the assignment.
    Returns:
        (passed, feedback_html)
        passed: Boolean, True if all tests passed
        feedback_html: String, HTML formatted feedback
    """
    code = submission.code
    test_cases = submission.assignment.test_cases.all()
    
    if not test_cases.exists():
        # If no test cases, we can't auto-mark. Treat as manual submission.
        return True, "No test cases defined. Submitted for manual grading."

    feedback = []
    all_passed = True

    for i, test in enumerate(test_cases, 1):
        try:
            # Run the code in a subprocess
            # We use the same python interpreter as the running process
            result = subprocess.run(
                [sys.executable, "-c", code],
                input=test.input_text,
                capture_output=True,
                text=True,
                timeout=2,  # 2 second timeout to prevent infinite loops
            )
            
            # Check for runtime errors
            if result.returncode != 0:
                all_passed = False
                feedback.append(f"❌ <strong>Test Case {i} Failed (Runtime Error):</strong><br>")
                feedback.append(f"<pre>{result.stderr}</pre>")
                continue

            # Normalize outputs (strip whitespace for looser matching)
            actual = result.stdout.strip()
            expected = test.expected_output.strip()

            if actual == expected:
                feedback.append(f"✅ <strong>Test Case {i} Passed</strong>")
            else:
                all_passed = False
                feedback.append(f"❌ <strong>Test Case {i} Failed:</strong>")
                feedback.append(f"Expected:<br><pre>{expected}</pre>")
                feedback.append(f"Got:<br><pre>{actual}</pre>")

        except subprocess.TimeoutExpired:
            all_passed = False
            feedback.append(f"❌ <strong>Test Case {i} Failed (Timeout):</strong> Code took too long to run.")
        except Exception as e:
            all_passed = False
            feedback.append(f"❌ <strong>Test Case {i} Failed (System Error):</strong> {str(e)}")

    final_feedback = "<br><br>".join(feedback)
    return all_passed, mark_safe(final_feedback)

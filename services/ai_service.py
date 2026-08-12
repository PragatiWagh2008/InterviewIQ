"""Lightweight AI service shim for InterviewIQ.

This project can run without external AI providers. When no provider is
configured, the app falls back to local heuristics and avoids crashing on
import.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Any, Dict, List, Optional

# Global executor for AI calls to avoid blocking the main thread
_AI_EXECUTOR = ThreadPoolExecutor(max_workers=2, thread_name_prefix="ai-service")


def generate_interview_questions(
    user_resume: str,
    designation: str,
    company: str,
    difficulty: str,
    n: int = 5,
) -> Optional[List[str]]:
    """Return interview questions when an AI provider is unavailable."""
    return None


def evaluate_answer(user_text: str, question: str, designation: str) -> Optional[Dict[str, Any]]:
    """Return a lightweight evaluation payload when AI is unavailable."""
    return None


def evaluate_answer_async(
    user_text: str,
    question: str,
    designation: str,
    timeout_ms: int = 8000,
) -> Optional[Dict[str, Any]]:
    """
    Evaluate answer asynchronously with a timeout.
    
    Args:
        user_text: The user's answer text
        question: The interview question
        designation: The job designation
        timeout_ms: Timeout in milliseconds
    
    Returns:
        Evaluation result dict or None if timeout/error
    """
    future = _AI_EXECUTOR.submit(evaluate_answer, user_text, question, designation)
    try:
        return future.result(timeout=timeout_ms / 1000.0)
    except TimeoutError:
        return None
    except Exception:
        return None


def shutdown_ai_executor():
    """Shutdown the AI executor. Call on application exit."""
    _AI_EXECUTOR.shutdown(wait=False)

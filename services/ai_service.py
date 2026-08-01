"""Lightweight AI service shim for InterviewIQ.

This project can run without external AI providers. When no provider is
configured, the app falls back to local heuristics and avoids crashing on
import.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


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

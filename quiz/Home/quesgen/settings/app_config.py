from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, List

import streamlit as st


class QuizTimer(Enum):
    NO_LIMIT = "0"
    MINUTES_5 = "5"
    MINUTES_10 = "10"
    MINUTES_15 = "15"
    MINUTES_20 = "20"
    MINUTES_30 = "30"


class Difficulty(Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class Page(Enum):
    LOGIN = "login"
    REGISTER = "register"
    QUIZ = "quiz"
    QUIZ_FINE = "quiz_fine"
    REPORT = "report"
    UPLOAD = "upload"
    MANAGE_FILES = "manage_files"
    CONFIGURE = "configure"
    CONFIGURE_FINE = "configure_fine"
    HISTORY = "history"
    LOGOUT = "logout"
    ADMIN_DASHBOARD = "admin_dashboard"
    FINAL = "final"
    FINAL_QUIZ = "final_quiz"
    RETAKE_SCORE = "retake_score"


@dataclass
class AppSettings:
    app_name: str = "AI based Quiz Generation platform"
    description: str = "LLM integrated Question Generation & Answer Evaluation Platform"

    # Authentication
    authenticated: bool = False
    username: str = ""

    # File management
    uploaded_files: List[Any] = field(default_factory=list)
    selected_files: List[Any] = field(default_factory=list)
    uploader_key: int = 0

    # Quiz configuration
    num_questions: int = 5
    difficulty: Difficulty = Difficulty.MEDIUM

    # Quiz state
    current_question: int = 0
    questions: List[Any] = field(default_factory=list)
    answers: List[Any] = field(default_factory=list)
    quiz_started: bool = False
    quiz_completed: bool = False

    # Navigation and history
    page: Page = Page.LOGIN
    quiz_history: List[Any] = field(default_factory=list)
    current_quiz_saved: bool = False

    # UI state
    show_clear_confirm: bool = False
    show_clear_files_confirm: bool = False

    def to_session_dict(self) -> dict:
        """Convert to dictionary suitable for session state."""
        result = {}
        for key, value in self.__dict__.items():
            if key == "app_name":
                continue
            # Convert enums to their values
            if isinstance(value, Enum):
                result[key] = value.value
            else:
                result[key] = value
        return result


@dataclass
class HtmlContent:

    style: Path = Path("./static/html/style.html")

    @classmethod
    def get_content(cls, file_type: str) -> str:
        """
        Get content for any specified file type.
        """
        if not hasattr(cls, file_type):
            raise AttributeError(f"No file defined for '{file_type}'")
        file_path = getattr(cls, file_type)
        return file_path.read_text(encoding="utf-8")


def initialize_session_state():
    settings = AppSettings()
    for key, value in settings.to_session_dict().items():
        st.session_state.setdefault(key, value)

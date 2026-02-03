"""
ARM device support module for OneWordAI.
Provides whisper.cpp integration for Android/Termux where PyTorch is unavailable.
"""
import os
from pathlib import Path

# ARM module paths
ARM_DIR = Path(__file__).parent
MODELS_DIR = ARM_DIR / "models"
WHISPER_CPP_DIR = ARM_DIR / "whisper.cpp"

# Ensure directories exist
MODELS_DIR.mkdir(exist_ok=True)

# Model name mapping: PyTorch -> GGML
MODEL_MAPPING = {
    "tiny": "ggml-tiny.bin",
    "base": "ggml-base.bin",
    "small": "ggml-small.bin",
    "medium": "ggml-medium.bin",
    "large": "ggml-large-v3.bin",
    "large-v3": "ggml-large-v3.bin",
}


def is_whisper_cpp_installed() -> bool:
    """Check if whisper.cpp is installed and compiled."""
    main_binary = WHISPER_CPP_DIR / "main"
    return main_binary.exists() and main_binary.is_file()


def get_model_path(model_name: str) -> Path:
    """Get the path to a GGML model file."""
    ggml_name = MODEL_MAPPING.get(model_name, f"ggml-{model_name}.bin")
    return MODELS_DIR / ggml_name


def is_model_downloaded(model_name: str) -> bool:
    """Check if a model is already downloaded."""
    model_path = get_model_path(model_name)
    return model_path.exists() and model_path.stat().st_size > 1000000  # At least 1MB


__all__ = [
    "ARM_DIR",
    "MODELS_DIR",
    "WHISPER_CPP_DIR",
    "MODEL_MAPPING",
    "is_whisper_cpp_installed",
    "get_model_path",
    "is_model_downloaded",
]

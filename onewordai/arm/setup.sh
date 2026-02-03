#!/bin/bash
# Whisper.cpp installation script for ARM devices (Android/Termux)

set -e

echo "🚀 Installing Whisper.cpp for ARM devices..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WHISPER_DIR="$SCRIPT_DIR/whisper.cpp"

# Check if running on Termux
if [ -d "$PREFIX" ]; then
    echo "✅ Detected Termux environment"
    PKG_MANAGER="pkg"
else
    echo "📦 Detected standard Linux environment"
    PKG_MANAGER="apt-get"
fi

# Install dependencies
echo "📦 Installing build dependencies..."
if [ "$PKG_MANAGER" = "pkg" ]; then
    pkg update -y
    pkg install -y git cmake clang wget
else
    sudo apt-get update -y
    sudo apt-get install -y git cmake build-essential wget
fi

# Clone whisper.cpp if not already present
if [ ! -d "$WHISPER_DIR" ]; then
    echo "📥 Cloning whisper.cpp..."
    cd "$SCRIPT_DIR"
    git clone https://github.com/ggerganov/whisper.cpp.git
else
    echo "✅ whisper.cpp already cloned"
fi

# Compile whisper.cpp
echo "🔨 Compiling whisper.cpp..."
cd "$WHISPER_DIR"
make clean
make

# Verify compilation
if [ -f "$WHISPER_DIR/main" ]; then
    echo "✅ Whisper.cpp compiled successfully!"
else
    echo "❌ Compilation failed!"
    exit 1
fi

# Download base model by default
MODELS_DIR="$SCRIPT_DIR/models"
mkdir -p "$MODELS_DIR"

echo "📥 Downloading base model (ggml-base.bin)..."
if [ ! -f "$MODELS_DIR/ggml-base.bin" ]; then
    cd "$WHISPER_DIR"
    bash ./models/download-ggml-model.sh base
    mv models/ggml-base.bin "$MODELS_DIR/"
    echo "✅ Base model downloaded"
else
    echo "✅ Base model already exists"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "You can now use: onewordai process-arm <file>"
echo ""

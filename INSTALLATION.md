# 📦 Jarvis AI - Installation Guide

## 🚀 Quick Test (Current Status - 35% Complete)

The backend API is ready to test NOW! Follow these steps:

### Option 1: Test Backend API (Works Now!)

```bash
# Clone repository
git clone https://github.com/sphoorthiomsphoorthiom/jarvis-ai-assistant.git
cd jarvis-ai-assistant

# Install Python dependencies
pip install fastapi uvicorn pydantic numpy

# Start the server
python backend/orchestrator/main.py

# Test in another terminal:
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message":"Hello Jarvis!", "mode":"offline"}'
```

**API Endpoints Available:**
- `POST /chat` - Send messages to Jarvis
- `POST /feedback` - Submit ratings (1-5 stars)
- `GET /health` - Check system status
- `GET /stats` - View learning statistics
- `WebSocket /ws` - Real-time bidirectional chat

---

## 📱 Android Installation (Coming Soon)

### Current Status: Need to build

**To Build Android APK:**

```bash
# 1. Install Flutter (if not installed)
curl -O https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.16.0-stable.tar.xz
tar xf flutter_linux_3.16.0-stable.tar.xz
export PATH="$PATH:`pwd`/flutter/bin"

# 2. Create Flutter project (coming in next update)
cd jarvis-ai-assistant
flutter create mobile
cd mobile

# 3. Add dependencies to pubspec.yaml:
# - http: ^1.1.0
# - web_socket_channel: ^2.4.0  
# - speech_to_text: ^6.5.1
# - flutter_tts: ^3.8.3

# 4. Build APK
flutter build apk --release

# APK will be at: build/app/outputs/flutter-apk/app-release.apk
```

**System Requirements:**
- Android 6.0 (API level 23) or higher
- 4GB RAM minimum
- 500MB free storage

---

## 🎮 iOS Installation (Coming Soon)

### Current Status: Need to build

**To Build iOS App:**

```bash
# 1. Requires macOS with Xcode installed
cd jarvis-ai-assistant/mobile

# 2. Build iOS app
flutter build ios --release

# 3. Open in Xcode
open ios/Runner.xcworkspace

# 4. Sign and deploy to TestFlight or device
```

**System Requirements:**
- iOS 12.0 or later
- iPhone 6s or newer
- 4GB RAM minimum
- 500MB free storage

---

## 🖥️ Windows Installation

### Option A: Run Backend Server (Works Now!)

```bash
# Install Python 3.10+
winget install Python.Python.3.11

# Clone and run
git clone https://github.com/sphoorthiomsphoorthiom/jarvis-ai-assistant.git
cd jarvis-ai-assistant
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python backend/orchestrator/main.py
```

Access at: http://localhost:8000

### Option B: Build Windows Desktop App (Coming Soon)

```bash
# Build Flutter Windows app
cd mobile
flutter config --enable-windows-desktop
flutter build windows --release

# Executable at: build/windows/runner/Release/jarvis_ai.exe
```

**System Requirements:**
- Windows 10/11 (64-bit)
- 8GB RAM recommended
- 2GB free storage

---

## 🤖 Download AI Models

### Required: Qwen2.5 LLM (FREE - 3GB)

```bash
mkdir models
cd models

# Download from HuggingFace
wget https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF/resolve/main/qwen2_5-7b-instruct-q4_k_m.gguf
```

**Or download manually:**
1. Visit: https://huggingface.co/Qwen/Qwen2.5-7B-Instruct-GGUF
2. Download: `qwen2_5-7b-instruct-q4_k_m.gguf` (3.3GB)
3. Place in: `jarvis-ai-assistant/models/`

### Auto-Downloaded Models:
- **Whisper STT**: Downloads automatically on first use
- **Coqui TTS**: Downloads automatically on first use
- **SBERT Embeddings**: Downloads automatically

---

## ✅ What's Working RIGHT NOW:

1. **✅ FastAPI Backend Server**
   - REST API endpoints
   - WebSocket support
   - Health monitoring

2. **✅ Self-Learning System**
   - Learns from every 7 interactions
   - Tracks success rate
   - Saves knowledge to disk

3. **✅ Feedback Collection**
   - 1-5 star ratings
   - Automatic model improvement

4. **✅ Memory Persistence**
   - Conversation history
   - Learned patterns
   - Best practices database

---

## 🚧 What Needs to Be Added:

1. **RAG Document Search** - `backend/rag/rag_engine.py`
2. **Local LLM Integration** - `backend/llm/local_model.py`
3. **Voice Interface** - `backend/voice/voice_handler.py`
4. **Flutter Mobile UI** - `mobile/lib/main.dart`
5. **Windows Desktop App** - Flutter Windows build

All code is available in SETUP_GUIDE.md!

---

## 📊 Test the Working Features:

### 1. Start Backend
```bash
python backend/orchestrator/main.py
```

### 2. Send a Chat Message
```bash
curl -X POST http://localhost:8000/chat \\
  -H "Content-Type: application/json" \\
  -d '{"message":"What can you do?", "mode":"offline"}'
```

### 3. Check Statistics
```bash
curl http://localhost:8000/stats
```

### 4. Submit Feedback
```bash
curl -X POST http://localhost:8000/feedback \\
  -H "Content-Type: application/json" \\
  -d '{"session_id":"test", "message_id":"msg1", "rating":5}'
```

---

## 🔗 Build Status

| Platform | Status | Size | Ready to Test |
|----------|--------|------|---------------|
| Backend API | ✅ Ready | - | YES - localhost:8000 |
| Android APK | 🚧 Pending | ~50MB | Need to build |
| iOS App | 🚧 Pending | ~50MB | Need to build |
| Windows EXE | 🚧 Pending | ~80MB | Backend only |

---

## 📞 Support

**Issues?**
1. Check Python version: `python --version` (need 3.10+)
2. Verify dependencies: `pip list`
3. Check logs in terminal
4. Open issue: https://github.com/sphoorthiomsphoorthiom/jarvis-ai-assistant/issues

**Next Steps:**
1. Test the backend API (works now!)
2. Add remaining modules (see SETUP_GUIDE.md)
3. Build mobile apps (Flutter)
4. Download Qwen2.5 model
5. Deploy to Google Play / App Store

---

**Repository**: https://github.com/sphoorthiomsphoorthiom/jarvis-ai-assistant

**Last Updated**: November 21, 2025

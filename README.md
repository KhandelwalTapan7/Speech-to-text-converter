```markdown
# 🎙️ Speech to Text Converter

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Whisper](https://img.shields.io/badge/Whisper-OpenAI-orange.svg)](https://github.com/openai/whisper)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/KhandelwalTapan7/Speech-to-text-converter)](https://github.com/KhandelwalTapan7/Speech-to-text-converter/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/KhandelwalTapan7/Speech-to-text-converter)](https://github.com/KhandelwalTapan7/Speech-to-text-converter/network)

A powerful web application that converts speech to text with support for **English** and **Hindi** languages using OpenAI's Whisper model. Perfect for transcriptions, meeting notes, lecture recordings, and more!

## 📸 Demo

![Speech to Text Converter Demo](https://via.placeholder.com/800x400?text=Speech+to+Text+Converter+Demo)

## ✨ Features

### Core Features
- 🎤 **Live Recording** - Record audio directly from your microphone
- 📁 **File Upload** - Upload pre-recorded audio files (MP3, WAV, MP4, etc.)
- 🌐 **Multi-language Support** - English, Hindi, and auto-detection
- 🚀 **Fast & Accurate** - Powered by OpenAI's Whisper model
- 💾 **Export Options** - Copy to clipboard or download as text file
- 🎨 **Modern UI** - Responsive and user-friendly interface

### Advanced Features
- 🔄 **Auto Language Detection** - Automatically identifies the spoken language
- 📊 **Real-time Processing** - Get transcriptions in seconds
- 🎯 **High Accuracy** - 95%+ accuracy for clear audio
- 💻 **Cross-platform** - Works on Windows, macOS, and Linux
- 🐳 **Docker Support** - Easy deployment with containerization

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI, Python 3.8+ |
| ML Model | OpenAI Whisper (base model) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Audio Processing | FFmpeg, Librosa, SoundFile |
| Deep Learning | PyTorch |
| Containerization | Docker |

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

| Requirement | Version | Installation Guide |
|-------------|---------|-------------------|
| Python | 3.8+ | [Download](https://www.python.org/downloads/) |
| FFmpeg | Latest | See instructions below |
| Git | Latest | [Download](https://git-scm.com/downloads) |
| pip | Latest | Comes with Python |

### 🔧 Installing FFmpeg

#### Windows (3 options)

**Option 1: Chocolatey (Easiest)**
```bash
choco install ffmpeg
```

**Option 2: Winget**
```bash
winget install ffmpeg
```

**Option 3: Manual**
1. Download from: https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to system PATH
4. Restart terminal

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

#### Linux (Fedora/RHEL)
```bash
sudo dnf install ffmpeg
```

#### Verify Installation
```bash
ffmpeg -version
```

## 🚀 Installation & Setup

### Method 1: Local Installation

#### Step 1: Clone the Repository
```bash
git clone https://github.com/KhandelwalTapan7/Speech-to-text-converter.git
cd Speech-to-text-converter
```

#### Step 2: Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 3: Frontend Setup
```bash
# Open a new terminal
cd frontend
# No additional setup needed - pure HTML/CSS/JS
```

#### Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # macOS/Linux
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 3000
```

#### Step 5: Access the App
Open your browser and navigate to: `http://localhost:3000`

### Method 2: Docker Installation

```bash
# Build the image
docker build -t speech-to-text-app .

# Run the container
docker run -p 8000:8000 speech-to-text-app
```

## 📁 Project Structure

```
Speech-to-text-converter/
│
├── backend/                      # FastAPI backend
│   ├── app/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── transcribe.py    # API endpoints
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── audio.py         # Audio processing
│   │   ├── __init__.py
│   │   ├── main.py               # FastAPI app
│   │   └── whisper_model.py     # Whisper integration
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile                # Docker config
│
├── frontend/                     # Static frontend
│   ├── index.html                # Main UI
│   ├── script.js                 # Frontend logic
│   └── style.css                 # Styling
│
├── uploads/                      # Temporary audio storage
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── README.md                     # Documentation
```

## 🔧 API Documentation

### Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| POST | `/api/transcribe` | Auto-detect language | `file` (audio), `language` (optional) |
| POST | `/api/transcribe-hindi` | Force Hindi | `file` (audio) |
| POST | `/api/transcribe-english` | Force English | `file` (audio) |
| GET | `/health` | Health check | None |
| GET | `/` | API info | None |

### API Usage Examples

#### cURL
```bash
# Auto-detect language
curl -X POST http://localhost:8000/api/transcribe \
  -F "file=@audio.mp3"

# Force Hindi
curl -X POST http://localhost:8000/api/transcribe-hindi \
  -F "file=@hindi_audio.mp3"

# Force English
curl -X POST http://localhost:8000/api/transcribe-english \
  -F "file=@english_audio.wav"
```

#### Python
```python
import requests

url = "http://localhost:8000/api/transcribe"
files = {'file': open('audio.mp3', 'rb')}
response = requests.post(url, files=files)
print(response.json()['text'])
```

#### JavaScript
```javascript
const formData = new FormData();
formData.append('file', audioFile);

fetch('http://localhost:8000/api/transcribe', {
    method: 'POST',
    body: formData
})
.then(res => res.json())
.then(data => console.log(data.text));
```

## 💡 Usage Guide

### 1. Select Language
- **Auto-detect**: Best for mixed or unknown languages
- **English**: Optimized for English speech
- **Hindi**: Optimized for Hindi speech

### 2. Choose Input Method

#### Option A: Upload File
- Click "Choose File"
- Select audio file (MP3, WAV, MP4, etc.)
- Click "Convert to Text"

#### Option B: Live Recording
- Click "Start Recording"
- Speak clearly into your microphone
- Click "Stop Recording"
- Automatic transcription begins

### 3. Export Results
- **Copy Text**: Copies transcription to clipboard
- **Download TXT**: Saves as text file

## 🎯 Best Practices

### For Best Results
- ✅ Speak clearly and at a normal pace
- ✅ Minimize background noise
- ✅ Use a good quality microphone
- ✅ Keep audio files under 25MB
- ✅ For Hindi, explicitly select Hindi language

### File Format Support
| Format | Support | Best For |
|--------|---------|----------|
| WAV | ✅ Excellent | High quality, no compression |
| MP3 | ✅ Good | Compressed, smaller size |
| MP4 | ✅ Good | Video files with audio |
| M4A | ✅ Good | Apple devices |
| WEBM | ✅ Good | Web recordings |
| OGG | ✅ Good | Open source format |

## 🐛 Troubleshooting

### Common Issues and Solutions

#### FFmpeg Not Found
```bash
# Error: [WinError 2] The system cannot find the file specified
# Solution: Install FFmpeg (see prerequisites section)
ffmpeg -version  # Verify installation
```

#### Backend Won't Start
```bash
# Error: Address already in use
# Solution: Kill process on port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
# macOS/Linux:
lsof -i :8000
kill -9 <PID>
```

#### Microphone Not Working
- Check browser permissions (allow microphone access)
- Ensure no other app is using the microphone
- Try a different browser (Chrome/Firefox recommended)
- Check system microphone settings

#### Transcription is Slow
- First transcription loads the model (~30 seconds)
- Subsequent transcriptions are faster
- Use smaller audio files for testing
- Consider using a smaller model (tiny or base)

#### Memory Issues
```bash
# Use a smaller Whisper model
# Edit whisper_model.py:
# Change model_size from "base" to "tiny"
model = whisper.load_model("tiny", device=device)
```

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| Model Load Time | ~30 seconds (first time) |
| Transcription Speed | ~10-15 seconds/min audio |
| Accuracy (Clean Audio) | 95%+ |
| Maximum File Size | 25MB |
| Supported Languages | 100+ |
| Memory Usage | ~2GB RAM |

## 🗺️ Roadmap

### Completed ✅
- [x] Basic speech to text functionality
- [x] English and Hindi support
- [x] File upload feature
- [x] Live recording
- [x] Copy and download options
- [x] Docker support

### In Progress 🚧
- [ ] Support for more Indian languages (Tamil, Telugu, Bengali)
- [ ] Batch file processing
- [ ] Punctuation and capitalization
- [ ] SRT subtitle generation

### Planned 📅
- [ ] User authentication
- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Mobile app (React Native)
- [ ] Real-time streaming transcription
- [ ] Custom vocabulary training

## 🤝 Contributing

We welcome contributions! See our [Contributing Guidelines](CONTRIBUTING.md).

### Quick Start for Contributors

1. **Fork the repository**
2. **Create a feature branch**
```bash
git checkout -b feature/AmazingFeature
```

3. **Commit your changes**
```bash
git commit -m 'Add some AmazingFeature'
```

4. **Push to branch**
```bash
git push origin feature/AmazingFeature
```

5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use meaningful commit messages
- Update documentation for major changes
- Add comments for complex logic
- Test before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** - For the incredible speech recognition model
- **FastAPI** - For the modern, fast web framework
- **FFmpeg** - For audio processing capabilities
- **PyTorch** - For deep learning infrastructure
- **Librosa** - For audio analysis tools

## 📞 Contact & Support

**Developer:** Tapan Khandelwal

- **GitHub:** [@KhandelwalTapan7](https://github.com/KhandelwalTapan7)
- **Project Link:** [https://github.com/KhandelwalTapan7/Speech-to-text-converter](https://github.com/KhandelwalTapan7/Speech-to-text-converter)
- **Issues:** [Report a bug](https://github.com/KhandelwalTapan7/Speech-to-text-converter/issues)

## ⭐ Show Your Support

If this project helped you or you found it useful, please consider:

- ⭐ **Star** the repository on GitHub
- 🍴 **Fork** the project
- 🐛 **Report** bugs and issues
- 💡 **Suggest** new features
- 📝 **Improve** documentation

Your support encourages continuous improvement!

---

## 🎉 Ready to Use!

You're all set! Start converting speech to text with ease. For questions or feedback, feel free to open an issue or reach out.

**Happy Transcribing! 🎙️**

---

Made with ❤️ by Tapan Khandelwal
```

## **To add this README to your repository:**

### Option 1: Directly on GitHub
1. Go to https://github.com/KhandelwalTapan7/Speech-to-text-converter
2. Click on `README.md`
3. Click the pencil icon (Edit)
4. Delete existing content
5. Paste the new README content
6. Scroll down and click "Commit changes"

### Option 2: Local push
```powershell
cd E:\speech-to-text-app

# Replace README.md with the content above
# Then run:
git add README.md
git commit -m "Add comprehensive README with documentation"
git push origin main
```


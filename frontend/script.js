const API_URL = 'http://localhost:8000/api';

let mediaRecorder = null;
let audioChunks = [];
let isRecording = false;
let currentAudioBlob = null;

// DOM Elements
const languageSelect = document.getElementById('language');
const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const uploadBtn = document.getElementById('uploadBtn');
const audioFile = document.getElementById('audioFile');
const fileName = document.getElementById('fileName');
const transcribeBtn = document.getElementById('transcribeBtn');
const progressSection = document.getElementById('progressSection');
const resultDiv = document.getElementById('result');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const recordingStatus = document.getElementById('recordingStatus');

// Event Listeners
recordBtn.addEventListener('click', startRecording);
stopBtn.addEventListener('click', stopRecording);
uploadBtn.addEventListener('click', () => audioFile.click());
audioFile.addEventListener('change', handleFileSelect);
transcribeBtn.addEventListener('click', transcribeAudio);
copyBtn.addEventListener('click', copyToClipboard);
downloadBtn.addEventListener('click', downloadText);

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        
        mediaRecorder.onstop = () => {
            currentAudioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            const audioFile = new File([currentAudioBlob], 'recording.wav', { type: 'audio/wav' });
            handleFile(audioFile);
            stream.getTracks().forEach(track => track.stop());
            recordingStatus.classList.remove('active');
            recordingStatus.style.display = 'none';
        };
        
        mediaRecorder.start();
        isRecording = true;
        recordBtn.disabled = true;
        stopBtn.disabled = false;
        recordingStatus.textContent = '🔴 Recording in progress... Speak clearly!';
        recordingStatus.style.display = 'block';
        recordingStatus.classList.add('active');
        
    } catch (error) {
        console.error('Error accessing microphone:', error);
        alert('Unable to access microphone. Please check permissions.');
    }
}

function stopRecording() {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();
        isRecording = false;
        recordBtn.disabled = false;
        stopBtn.disabled = true;
    }
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        handleFile(file);
    }
}

function handleFile(file) {
    currentAudioBlob = file;
    fileName.textContent = file.name;
    transcribeBtn.disabled = false;
    
    // Clear previous result
    resultDiv.innerHTML = '<p class="placeholder">Your transcribed text will appear here...</p>';
    copyBtn.disabled = true;
    downloadBtn.disabled = true;
}

async function transcribeAudio() {
    if (!currentAudioBlob) {
        alert('Please select or record an audio file first');
        return;
    }
    
    const language = languageSelect.value;
    const endpoint = language === 'auto' ? '/transcribe' : 
                    language === 'hi' ? '/transcribe-hindi' : '/transcribe-english';
    
    const formData = new FormData();
    formData.append('file', currentAudioBlob);
    
    // Show progress
    progressSection.style.display = 'block';
    transcribeBtn.disabled = true;
    resultDiv.innerHTML = '<p class="placeholder">Processing...</p>';
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResult(data.text);
            copyBtn.disabled = false;
            downloadBtn.disabled = false;
        } else {
            throw new Error(data.detail || 'Transcription failed');
        }
        
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `<p class="error" style="color: red;">Error: ${error.message}<br>Please make sure the backend server is running.</p>`;
    } finally {
        progressSection.style.display = 'none';
        transcribeBtn.disabled = false;
    }
}

function displayResult(text) {
    resultDiv.innerHTML = `<p>${escapeHtml(text)}</p>`;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function copyToClipboard() {
    const text = resultDiv.innerText;
    try {
        await navigator.clipboard.writeText(text);
        showTemporaryMessage('Copied to clipboard!', copyBtn);
    } catch (err) {
        alert('Failed to copy text');
    }
}

function downloadText() {
    const text = resultDiv.innerText;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `transcript_${new Date().toISOString().slice(0,19)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function showTemporaryMessage(message, button) {
    const originalText = button.textContent;
    button.textContent = message;
    setTimeout(() => {
        button.textContent = originalText;
    }, 2000);
}

// Check backend health
async function checkBackendHealth() {
    try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
            console.log('Backend is healthy');
        }
    } catch (error) {
        console.warn('Backend not running. Please start the backend server.');
    }
}

checkBackendHealth();
/**
 * Frontend JavaScript for OneWord AI
 * Handles file upload, API communication, and UI updates
 */

// ========== STATE ==========
let uploadedFileId = null;
let currentJobId = null;
let pollingInterval = null;

// ========== DOM ELEMENTS ==========
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const processBtn = document.getElementById('processBtn');
const progressCard = document.getElementById('progressCard');
const downloadCard = document.getElementById('downloadCard');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const statusText = document.getElementById('statusText');
const downloadBtn = document.getElementById('downloadBtn');
const resetBtn = document.getElementById('resetBtn');
const instaPopup = document.getElementById('instaPopup');
const closePopup = document.getElementById('closePopup');

const modelSelect = document.getElementById('modelSelect');
const languageSelect = document.getElementById('languageSelect');
const modeSelect = document.getElementById('modeSelect');

// ========== FILE UPLOAD ==========
dropzone.addEventListener('click', () => {
    fileInput.click();
});

dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

async function handleFile(file) {
    // Validate file size (100MB limit)
    const maxSize = 100 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('File too large! Maximum size is 100MB.');
        return;
    }

    // Show file info
    fileName.textContent = `📁 ${file.name}`;
    fileSize.textContent = `📊 ${formatFileSize(file.size)}`;
    fileInfo.classList.remove('hidden');

    // Upload file
    statusText.textContent = 'Uploading...';
    progressCard.classList.remove('hidden');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Upload failed');
        }

        const data = await response.json();
        uploadedFileId = data.file_id;

        // Enable process button
        processBtn.disabled = false;
        progressCard.classList.add('hidden');

    } catch (error) {
        alert('Upload failed: ' + error.message);
        progressCard.classList.add('hidden');
    }
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

// ========== PROCESSING ==========
processBtn.addEventListener('click', async () => {
    if (!uploadedFileId) {
        alert('Please upload a file first');
        return;
    }

    // Get config
    const model = modelSelect.value;
    const language = languageSelect.value || null;
    const mode = modeSelect.value;

    // Start processing
    const formData = new FormData();
    formData.append('file_id', uploadedFileId);
    formData.append('model', model);
    if (language) {
        formData.append('language', language);
    }
    formData.append('mode', mode);

    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Processing failed to start');
        }

        const data = await response.json();
        currentJobId = data.job_id;

        // Show progress card
        progressCard.classList.remove('hidden');
        processBtn.disabled = true;

        // Start polling
        startPolling();

    } catch (error) {
        alert('Error: ' + error.message);
    }
});

// ========== POLLING ==========
// ========== POLLING ==========
let simulatedProgress = 0;

function startPolling() {
    simulatedProgress = 0;

    // Status polling
    pollingInterval = setInterval(async () => {
        try {
            const response = await fetch(`/api/status/${currentJobId}`);

            if (response.status === 404) {
                stopPolling();
                alert('Connection lost or server restarted. Please try uploading again.');
                resetUI();
                return;
            }

            if (!response.ok) {
                throw new Error('Status check failed');
            }

            const job = await response.json();

            // Update UI
            updateProgress(job);

            // Check if complete
            if (job.status === 'completed') {
                stopPolling();
                // Force 100% just in case
                progressFill.style.width = '100%';
                progressText.textContent = '100%';
                setTimeout(() => showDownload(), 500);
            } else if (job.status === 'failed') {
                stopPolling();
                alert('Processing failed: ' + job.error);
                resetUI();
            }

        } catch (error) {
            console.error('Polling error:', error);
        }
    }, 1000);

    // Simulate progress animation
    simulationInterval = setInterval(() => {
        if (simulatedProgress < 90) {
            // Slower progress as it gets higher
            const increment = simulatedProgress < 30 ? 2 : (simulatedProgress < 60 ? 1 : 0.5);
            simulatedProgress += increment;

            // Only update visualization if real progress isn't higher
            const currentReal = parseFloat(progressFill.style.width) || 0;
            if (simulatedProgress > currentReal) {
                progressFill.style.width = simulatedProgress + '%';
                progressText.textContent = Math.round(simulatedProgress) + '%';
            }
        }
    }, 500);
}

let simulationInterval = null;

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
    if (simulationInterval) {
        clearInterval(simulationInterval);
        simulationInterval = null;
    }
}

function updateProgress(job) {
    const realProgress = job.progress || 0;

    // If real progress is reported (e.g. from backend), use it if it's high enough
    // Otherwise rely on simulation
    if (realProgress > simulatedProgress) {
        simulatedProgress = realProgress; // Sync simulation
        progressFill.style.width = realProgress + '%';
        progressText.textContent = Math.round(realProgress) + '%';
    }

    // Update status text
    if (job.status === 'processing') {
        statusText.textContent = '🧠 Transcribing with Whisper... (This may take a moment)';
    } else if (job.status === 'pending') {
        statusText.textContent = '⏳ Waiting to start...';
    }
}

function showDownload() {
    progressCard.classList.add('hidden');
    downloadCard.classList.remove('hidden');

    // Show Instagram popup after 2 seconds
    setTimeout(() => {
        instaPopup.classList.remove('hidden');
    }, 2000);
}

// ========== DOWNLOAD ==========
downloadBtn.addEventListener('click', () => {
    if (currentJobId) {
        window.location.href = `/api/download/${currentJobId}`;
    }
});

// ========== RESET ==========
resetBtn.addEventListener('click', () => {
    resetUI();
});

function resetUI() {
    uploadedFileId = null;
    currentJobId = null;
    fileInfo.classList.add('hidden');
    progressCard.classList.add('hidden');
    downloadCard.classList.add('hidden');
    processBtn.disabled = true;
    progressFill.style.width = '0%';
    progressText.textContent = '0%';
    fileInput.value = '';
}

// ========== POPUP ==========
closePopup.addEventListener('click', () => {
    instaPopup.classList.add('hidden');
});

instaPopup.addEventListener('click', (e) => {
    if (e.target === instaPopup) {
        instaPopup.classList.add('hidden');
    }
});

// Show popup on load
setTimeout(() => {
    instaPopup.classList.remove('hidden');
}, 1000);

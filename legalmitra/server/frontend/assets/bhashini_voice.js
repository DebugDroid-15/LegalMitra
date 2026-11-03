// Digital India Bhashini Voice Dictation (Phase 93)
let isRecordingAudio = false;
let mediaRecorder = null;
let audioChunks = [];

window.toggleSpeech = async function() {
    const micBtn = document.querySelector('button[title="Voice Input"]');
    const inputField = document.getElementById('stitch-query-input');
    
    if (!isRecordingAudio) {
        try {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                
                mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) audioChunks.push(event.data);
                };
                
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = async () => {
                        const base64Audio = reader.result;
                        if (micBtn) micBtn.innerHTML = '<span class="material-symbols-outlined text-[20px] animate-spin">sync</span>';
                        try {
                            const res = await fetch('/api/v1/voice/transcribe', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ audio_base64: base64Audio, language: 'mr' })
                            });
                            const data = await res.json();
                            if (data.transcription && inputField) {
                                inputField.value = data.transcription;
                                inputField.focus();
                            }
                        } catch (err) {
                            console.error('ASR transcription error:', err);
                        } finally {
                            if (micBtn) {
                                micBtn.innerHTML = '<span class="material-symbols-outlined text-[20px]">mic</span>';
                                micBtn.classList.remove('bg-red-500', 'text-white');
                            }
                        }
                    };
                };
                
                mediaRecorder.start();
                isRecordingAudio = true;
                if (micBtn) {
                    micBtn.classList.add('bg-red-500', 'text-white');
                    micBtn.innerHTML = '<span class="material-symbols-outlined text-[20px] animate-pulse">mic</span>';
                }
            } else {
                throw new Error("getUserMedia not supported");
            }
        } catch (err) {
            console.warn('Microphone error or permission denied, using simulated Indic ASR prompt:', err);
            // Simulated voice input for local environments
            if (inputField) {
                inputField.value = 'पोलीस ठाण्यात एफआयआर नोंदवून घेण्यास नकार दिल्यास कायदेशीर प्रक्रिया काय आहे?';
                inputField.focus();
            }
        }
    } else {
        if (mediaRecorder && mediaRecorder.state !== 'inactive') {
            mediaRecorder.stop();
        }
        isRecordingAudio = false;
        if (micBtn) {
            micBtn.classList.remove('bg-red-500', 'text-white');
            micBtn.innerHTML = '<span class="material-symbols-outlined text-[20px]">mic</span>';
        }
    }
};

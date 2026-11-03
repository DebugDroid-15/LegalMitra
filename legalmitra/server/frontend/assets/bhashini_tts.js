// Digital India Bhashini TTS Audio Readout Controller (Phase 96)
window.speakLegalText = async function(buttonElement, rawText, language = 'mr') {
    if (!buttonElement || !rawText) return;
    const originalHtml = buttonElement.innerHTML;
    buttonElement.innerHTML = '<span class="material-symbols-outlined text-[16px] animate-spin text-primary">sync</span>';
    buttonElement.disabled = true;

    try {
        const res = await fetch('/api/v1/voice/synthesize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: rawText, language: language, gender: 'female' })
        });
        const data = await res.json();
        if (data.success && data.audio_base64) {
            // Play synthesized audio stream via HTML5 Audio element
            const audio = new Audio("data:audio/wav;base64," + data.audio_base64);
            buttonElement.innerHTML = '<span class="material-symbols-outlined text-[16px] text-primary animate-pulse">volume_up</span>';
            audio.play();
            audio.onended = () => {
                buttonElement.innerHTML = originalHtml;
                buttonElement.disabled = false;
            };
        } else {
            // Web Speech API fallback for local browser readout
            const utterance = new SpeechSynthesisUtterance(rawText.replace(/[*#_`]/g, ''));
            utterance.lang = language === 'mr' ? 'mr-IN' : language === 'hi' ? 'hi-IN' : 'en-IN';
            window.speechSynthesis.speak(utterance);
            buttonElement.innerHTML = originalHtml;
            buttonElement.disabled = false;
        }
    } catch (e) {
        console.warn('Bhashini TTS network synthesis error, falling back to Web Speech API:', e);
        const utterance = new SpeechSynthesisUtterance(rawText.replace(/[*#_`]/g, ''));
        window.speechSynthesis.speak(utterance);
        buttonElement.innerHTML = originalHtml;
        buttonElement.disabled = false;
    }
};

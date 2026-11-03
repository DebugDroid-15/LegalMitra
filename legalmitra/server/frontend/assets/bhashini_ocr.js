// Digital India Bhashini Document OCR Handler (Phase 94)
window.handleFileSelected = async function(fileInput) {
    if (!fileInput || !fileInput.files || fileInput.files.length === 0) return;
    const file = fileInput.files[0];
    const inputField = document.getElementById('stitch-query-input');
    const attachBtn = document.querySelector('button[title="Upload Case PDF, FIR, or Agreement"]');

    if (attachBtn) {
        attachBtn.innerHTML = '<span class="material-symbols-outlined text-[20px] animate-spin text-primary">sync</span>';
    }

    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = async () => {
        const base64Doc = reader.result;
        try {
            const res = await fetch('/api/v1/document/ocr-analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ document_base64: base64Doc, language: 'mr' })
            });
            const data = await res.json();
            if (data.success && inputField) {
                let prompt = `[दस्तऐवज विश्लेषण / Document Analysis: ${data.document_type}]\n`;
                if (data.detected_statutes && data.detected_statutes.length > 0) {
                    const provisions = data.detected_statutes.map(s => s.normalized_canonical).join(', ');
                    prompt += `आढळलेली कलमे (Identified Sections): ${provisions}\n`;
                }
                prompt += `दस्तऐवजातील सारांश:\n${data.extracted_text}\n\nकृपया या दस्तावेजाबाबत कायदेशीर अधिकार व पुढील प्रक्रिया स्पष्ट करा.`;
                inputField.value = prompt;
                inputField.focus();
            }
        } catch (err) {
            console.error('Document OCR error:', err);
        } finally {
            if (attachBtn) {
                attachBtn.innerHTML = '<span class="material-symbols-outlined text-[20px]">attach_file</span>';
            }
            fileInput.value = '';
        }
    };
};

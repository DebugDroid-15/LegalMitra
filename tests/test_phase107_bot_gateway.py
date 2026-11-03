"""
Unit tests for Phase 107: WhatsApp & Telegram Sovereign Voice Bot Integration.
"""
import pytest
from legalmitra.integrations.bot_gateway import sovereign_bot_gateway, InboundBotMessage

def test_bot_webhook_marathi_voice():
    msg = InboundBotMessage(
        channel="whatsapp",
        sender_id="+919876543210",
        message_type="voice",
        text_content="पोलीस ठाण्यात एफआयआर नोंदवून घेण्यास नकार दिला आहे काय करावे?",
        language_code="mr"
    )
    resp = sovereign_bot_gateway.process_inbound(msg)
    assert resp.recipient_id == "+919876543210"
    assert "पोलीस" in resp.reply_text
    assert any("Section 173(4)" in c for c in resp.statutory_citations)
    assert resp.voice_audio_base64 is not None
    assert any("IndicTTS" in step for step in resp.processing_pipeline)

def test_bot_webhook_hindi_text():
    msg = InboundBotMessage(
        channel="telegram",
        sender_id="chat_987654",
        message_type="text",
        text_content="पुलिस एफआईआर नहीं लिख रही है",
        language_code="hi"
    )
    resp = sovereign_bot_gateway.process_inbound(msg)
    assert resp.recipient_id == "chat_987654"
    assert "प्राथमिकी" in resp.reply_text
    assert len(resp.action_buttons) > 0

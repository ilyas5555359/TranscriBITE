import asyncio

import pytest

from app.services.summary_service import SummaryService


def test_build_prompt_in_french():
    prompt = SummaryService._build_prompt("Bonjour", "fr")

    assert "en français" in prompt
    assert "1 à 2 lignes maximum" in prompt
    assert "20 mots maximum" in prompt
    assert "Bonjour" in prompt


def test_build_prompt_in_english():
    prompt = SummaryService._build_prompt("Hello", "en")

    assert "Summarize" in prompt
    assert "1 to 2 lines" in prompt
    assert "20 words maximum" in prompt
    assert "Hello" in prompt


def test_build_prompt_in_arabic():
    prompt = SummaryService._build_prompt("مرحبا بكم", "ar")

    assert "باللغة العربية" in prompt
    assert "20 كلمة" in prompt
    assert "مرحبا بكم" in prompt


def test_empty_text_is_rejected():
    with pytest.raises(ValueError):
        asyncio.run(SummaryService().generate_summary("  "))

"""Tests for Have I Been Pwned (HIBP) k-anonymity protocol."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from lib.pwned import check_single_password_breached, check_wordlist_pwned


def test_hibp_k_anonymity_breached() -> None:
    """Verify SHA-1 hash prefix/suffix matching when password is found."""
    password_to_test = "password123"
    full_hash = hashlib.sha1(password_to_test.encode("utf-8")).hexdigest().upper()
    prefix = full_hash[:5]
    suffix = full_hash[5:]

    mock_api_body = f"00000000000000000000000000000000000:1\n{suffix}:492021\n11111111111111111111111111111111111:5"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_api_body

    with patch("requests.get", return_value=mock_response) as mocked_get:
        is_breached, breach_count = check_single_password_breached(password_to_test)
        assert is_breached is True
        assert breach_count == 492021
        # Ensure only the 5-character prefix was sent in URL, not full hash or password!
        called_url = mocked_get.call_args[0][0]
        assert prefix in called_url
        assert suffix not in called_url
        assert password_to_test not in called_url


def test_hibp_k_anonymity_clean() -> None:
    """Verify clean response when hash suffix is not in returned list."""
    password_to_test = "SuperUnlikelyRandomString991823"
    mock_api_body = "00000000000000000000000000000000000:1\n11111111111111111111111111111111111:5"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = mock_api_body

    with patch("requests.get", return_value=mock_response):
        is_breached, breach_count = check_single_password_breached(password_to_test)
        assert is_breached is False
        assert breach_count == 0


def test_hibp_wordlist_scan() -> None:
    """Verify streaming wordlist checking with mocked responses."""
    with tempfile.TemporaryDirectory() as temp_dir:
        wordlist_path = Path(temp_dir) / "wordlist.txt"
        compromised_path = Path(temp_dir) / "compromised.txt"

        test_word = "pwned_pass"
        word_hash = hashlib.sha1(test_word.encode("utf-8")).hexdigest().upper()
        suffix = word_hash[5:]

        wordlist_path.write_text(f"{test_word}\nclean_pass\n", encoding="utf-8")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = f"{suffix}:12"

        with patch("requests.get", return_value=mock_response):
            total_checked, total_breached = check_wordlist_pwned(
                wordlist_path=wordlist_path,
                output_compromised_path=compromised_path,
                delay_between_requests=0.0,
            )
            assert total_checked == 2
            assert total_breached == 1
            output_content = compromised_path.read_text(encoding="utf-8")
            assert f"{test_word}:12" in output_content

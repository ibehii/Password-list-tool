#  GitHub: https://github.com/ibehii
#  Telegram: https://t.me/dr_xz
#  ____________________________________________
"""Have I Been Pwned (HIBP) k-anonymity password breach checking.

Uses the SHA-1 k-anonymity protocol where only the first 5 characters of the SHA-1 hash
are transmitted to the API. The password itself is NEVER sent over the network.
"""

from __future__ import annotations

import hashlib
import time
from collections import OrderedDict
from pathlib import Path
from typing import Callable, Optional

import requests

HIBP_API_URL = "https://api.pwnedpasswords.com/range/{prefix}"
USER_AGENT = "Password-List-Tool-SecCheck/2.0"
MAX_PREFIX_CACHE_ENTRIES = 2048


def check_single_password_breached(password: str, timeout_seconds: int = 10) -> tuple[bool, int]:
    """Check if a password has appeared in data breaches using HIBP k-anonymity.

    Returns: (is_breached, breach_count)
    """
    if not password:
        return False, 0

    full_sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = full_sha1[:5]
    suffix = full_sha1[5:]

    request_headers = {"User-Agent": USER_AGENT, "Add-Padding": "true"}
    url = HIBP_API_URL.format(prefix=prefix)

    try:
        response = requests.get(url, headers=request_headers, timeout=timeout_seconds)
        if response.status_code != 200:
            return False, 0
    except requests.RequestException:
        return False, 0

    for raw_line in response.text.splitlines():
        line_parts = raw_line.strip().split(":")
        if len(line_parts) == 2:
            returned_suffix, count_str = line_parts
            if returned_suffix.upper() == suffix:
                try:
                    return True, int(count_str)
                except ValueError:
                    return True, 1

    return False, 0


def check_wordlist_pwned(
    wordlist_path: Path,
    output_compromised_path: Path,
    max_check_count: int = 0,
    delay_between_requests: float = 0.1,
    session: Optional[requests.Session] = None,
    progress_callback: Optional[Callable[[int, int], None]] = None,
) -> tuple[int, int]:
    """Stream-check a wordlist against HIBP k-anonymity API.

    Uses a bounded LRU cache for prefix lookups to guarantee minimal memory.
    Supports optional requests.Session for persistent keep-alive connections.
    Returns: (total_checked, total_breached)
    """
    wordlist_path = Path(wordlist_path).resolve()
    output_compromised_path = Path(output_compromised_path).resolve()
    output_compromised_path.parent.mkdir(parents=True, exist_ok=True)

    prefix_cache: OrderedDict[str, dict[str, int]] = OrderedDict()
    total_checked = 0
    total_breached = 0

    http_client = session if session is not None else requests

    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as source_stream, \
         open(output_compromised_path, "w", encoding="utf-8") as output_stream:
        for line_content in source_stream:
            candidate_password = line_content.rstrip("\r\n")
            if not candidate_password:
                continue

            total_checked += 1
            full_sha1 = hashlib.sha1(candidate_password.encode("utf-8")).hexdigest().upper()
            prefix = full_sha1[:5]
            suffix = full_sha1[5:]

            if prefix in prefix_cache:
                prefix_cache.move_to_end(prefix)
                prefix_map = prefix_cache[prefix]
            else:
                url = HIBP_API_URL.format(prefix=prefix)
                request_headers = {"User-Agent": USER_AGENT, "Add-Padding": "true"}
                prefix_map = {}

                max_retries = 3
                retry_delay = 1.0
                for attempt_idx in range(max_retries):
                    try:
                        resp = http_client.get(url, headers=request_headers, timeout=10)
                        if resp.status_code == 200:
                            for item_line in resp.text.splitlines():
                                parts = item_line.strip().split(":")
                                if len(parts) == 2:
                                    try:
                                        prefix_map[parts[0].upper()] = int(parts[1])
                                    except ValueError:
                                        pass
                            break
                        elif resp.status_code == 429:
                            time.sleep(retry_delay)
                            retry_delay *= 2.0
                        else:
                            break
                    except requests.RequestException:
                        break

                prefix_cache[prefix] = prefix_map
                if len(prefix_cache) > MAX_PREFIX_CACHE_ENTRIES:
                    prefix_cache.popitem(last=False)

                if delay_between_requests > 0:
                    time.sleep(delay_between_requests)

            breach_count = prefix_map.get(suffix, 0)
            if breach_count > 0:
                output_stream.write(f"{candidate_password}:{breach_count}\n")
                total_breached += 1

            if progress_callback and total_checked % 25 == 0:
                progress_callback(total_checked, total_breached)

            if max_check_count > 0 and total_checked >= max_check_count:
                break

    return total_checked, total_breached

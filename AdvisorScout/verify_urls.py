"""Batch URL verification tool for universities.json."""
import requests
import json
import sys
from typing import Optional


def verify_urls(json_path: str = "universities.json", timeout: int = 10) -> int:
    """
    Verify all pending faculty URLs in universities.json.
    Updates status to 'verified' (200) or 'broken' (non-200 / error).
    Returns number of broken URLs.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    broken_count = 0
    total = 0

    for uni in data["universities"]:
        if uni["status"] not in ("pending", "broken"):
            continue
        total += 1
        name = uni["name"]
        url = uni["faculty_url"]
        try:
            resp = requests.head(url, timeout=timeout, allow_redirects=True,
                                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code == 200:
                uni["status"] = "verified"
                print(f"✅ {name}: 200 OK")
            else:
                uni["status"] = "broken"
                broken_count += 1
                print(f"❌ {name}: HTTP {resp.status_code}")
        except requests.exceptions.Timeout:
            uni["status"] = "broken"
            broken_count += 1
            print(f"❌ {name}: Timeout ({timeout}s)")
        except requests.exceptions.ConnectionError:
            uni["status"] = "broken"
            broken_count += 1
            print(f"❌ {name}: Connection refused")
        except Exception as e:
            uni["status"] = "broken"
            broken_count += 1
            print(f"❌ {name}: {str(e)[:80]}")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nDone: {total} checked, {total - broken_count} verified, {broken_count} broken")
    return broken_count


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "universities.json"
    sys.exit(verify_urls(path))

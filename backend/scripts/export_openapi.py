import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.main import app  # noqa: E402


def main() -> None:
    target = ROOT / 'openapi.json'
    target.write_text(json.dumps(app.openapi(), indent=2))
    print(f"wrote {target}")


if __name__ == '__main__':
    main()

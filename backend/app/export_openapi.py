import json
from pathlib import Path
from .main import app


def main() -> None:
    out = Path(__file__).resolve().parents[1] / "openapi.v2.6.json"
    out.write_text(json.dumps(app.openapi(), indent=2) + "\n")
    print(f"Wrote {out}")


if __name__ == '__main__':
    main()

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
PY = ROOT.parent / ".venv" / "Scripts" / "python.exe"


def indexed_runs():
    runs = {}
    for d in OUTPUT.glob("run_*"):
        idx = d / "index.json"
        if not idx.exists():
            continue
        try:
            data = json.loads(idx.read_text(encoding="utf-8"))
            runs[d.name] = data
        except Exception:
            continue
    return runs


def main():
    scopes = [s for s in range(5, 116, 5)] + [116]
    runs_before = indexed_runs()

    for scope in scopes:
        review_from = 0 if scope == 5 else scope - 5
        print(f"RUN scope={scope} review_from={review_from}", flush=True)

        cmd = [
            str(PY),
            "-m",
            "scrapy",
            "crawl",
            "fis_pilot",
            "-a",
            "seed_file=input/urls_master.txt",
            "-a",
            "exclude_file=input/urls_excluded.txt",
            "-a",
            f"scope_limit={scope}",
            "-a",
            f"review_from={review_from}",
            "-a",
            f"pilot_limit={scope}",
            "-a",
            "max_interactions=5",
            "-a",
            "only_new=true",
            "-s",
            "LOG_LEVEL=ERROR",
        ]
        proc = subprocess.run(cmd, cwd=ROOT)

        runs_after = indexed_runs()
        new_names = sorted(set(runs_after.keys()) - set(runs_before.keys()))

        valid = None
        for name in reversed(new_names):
            data = runs_after[name]
            sel = data.get("selection", {})
            if sel.get("scope_limit") == scope:
                valid = (name, data)
                break

        if valid is None:
            print(f"ERROR: no valid indexed run found for scope={scope}; process_exit={proc.returncode}", flush=True)
            raise SystemExit(2)

        name, data = valid
        if data.get("closed_reason") != "finished":
            print(f"ERROR: run {name} closed_reason={data.get('closed_reason')}", flush=True)
            raise SystemExit(3)

        print(
            f"OK run={name} scope={data['selection']['scope_limit']} pages={data.get('total_pages')} closed={data.get('closed_reason')} process_exit={proc.returncode}",
            flush=True,
        )
        runs_before = runs_after

    print("ALL_RUNS_COMPLETED", flush=True)


if __name__ == "__main__":
    main()

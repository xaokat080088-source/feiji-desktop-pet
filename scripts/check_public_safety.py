"""
公开版安全检查脚本
扫描项目目录中是否残留敏感信息
"""

import os
import sys
from pathlib import Path

SENSITIVE_PATTERNS = [
    "丁婉姗",
    "Jennie",
    "D:/feiji",
    "D:\\feiji",
    "sk-",
    'DEEPSEEK_API_KEY = "',
    "DEEPSEEK_API_KEY = '",
    'api_key = "',
    "去世",
    "天堂",
    "女朋友",
    "小二",
]

SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico",
    ".mp3", ".wav", ".ogg", ".flac",
    ".pyc", ".pyo", ".pyd",
    ".exe", ".dll", ".so",
    ".zip", ".tar", ".gz",
}

SKIP_DIRS = {
    "__pycache__", ".git", "node_modules", "build", "dist", "scripts",
}


def scan_file(filepath: Path) -> list:
    findings = []
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore")
        for pattern in SENSITIVE_PATTERNS:
            if pattern in text:
                findings.append((str(filepath), pattern))
    except Exception:
        pass
    return findings


def main():
    project_dir = Path(__file__).resolve().parent.parent
    print(f"Scanning: {project_dir}")
    print(f"Checking {len(SENSITIVE_PATTERNS)} sensitive patterns...\n")

    all_findings = []

    for root, dirs, files in os.walk(project_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in SKIP_EXTENSIONS:
                continue
            findings = scan_file(fpath)
            all_findings.extend(findings)

    if all_findings:
        print("WARNING: Sensitive content found!\n")
        for filepath, pattern in all_findings:
            rel = os.path.relpath(filepath, project_dir)
            print(f"  [{pattern}] in {rel}")
        print(f"\nTotal: {len(all_findings)} finding(s)")
        sys.exit(1)
    else:
        print("Public safety check PASSED. No sensitive content found.")
        sys.exit(0)


if __name__ == "__main__":
    main()

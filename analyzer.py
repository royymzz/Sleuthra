from pathlib import Path 
import hashlib 
import subprocess
import json
import argparse
from datetime import datetime

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

def detect_file_type(file_path):
    result = subprocess.run( 
        ["file", "-b", str(file_path)],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def check_extension_mismatch(file_path, detected_type):
    extension = file_path.suffix.lower()

    expected_types = {
        ".txt": ["text"],
        ".jpg": ["jpeg image"],
        ".jpeg": ["jpeg image"],
        ".png": ["png image"],
        ".pdf": ["pdf document"],
    }

    if extension not in expected_types:
        return False

    detected_lower = detected_type.lower()

    for expected in expected_types[extension]:
        if expected in detected_lower:
            return False

    return True

def check_file_signature(file_path):
    signatures = {
        ".pdf": [b"%PDF"],
        ".jpg": [b"\xff\xd8\xff"],
        ".jpeg": [b"\xff\xd8\xff"],
        ".png": [b"\x89PNG\r\n\x1a\n"],
        ".gif": [b"GIF87a", b"GIF89a"],
        ".zip": [b"PK\x03\x04"],
    }

    extension = file_path.suffix.lower()

    if extension not in signatures:
        return None

    with open(file_path, "rb") as file:
        header = file.read(16)

    for signature in signatures[extension]:
        if header.startswith(signature):
            return True

    return False

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Sleuthra - File Forensics Analyzer"
    )
    parser.add_argument(
        "scan_path",
        help="Directory containing files to analyze"
    )

    return parser.parse_args()

def analyze_file(file_path, scan_folder):
    findings = []

    print(f"Found file: {file_path.name}")
    print(f" Extension: {file_path.suffix}")
    print(f" Size: {file_path.stat().st_size} bytes")

    file_stats = file_path.stat()

    modified_time = datetime.fromtimestamp(
        file_stats.st_mtime
    ).strftime("%Y-%m-%d %H:%M:%S")

    accessed_time = datetime.fromtimestamp(
        file_stats.st_atime
    ).strftime("%Y-%m-%d %H:%M:%S")

    changed_time = datetime.fromtimestamp(
        file_stats.st_ctime
    ).strftime("%Y-%m-%d %H:%M:%S")
    
    print(f" Modified: {modified_time}")
    print(f" Accessed: {accessed_time}")
    print(f" Metadata changed: {changed_time}")

    file_hash = calculate_sha256(file_path)
    print(f" SHA-256: {file_hash}")

    detected_type = detect_file_type(file_path)
    print(f" Detected type: {detected_type}")

    signature_valid = check_file_signature(file_path)

    if signature_valid is True:
        print(" File signature: VALID")
    elif signature_valid is False:
        print(" File signature: INVALID")
    else: 
        print(" File signature: NOT CHECKED")
        
    mismatch = check_extension_mismatch(file_path, detected_type)

    if mismatch:
        findings.append(
            f"Extension mismatch: {file_path.suffix} extension, "
            f"but detected as {detected_type}"
        )

    if signature_valid is False:
        findings.append(
            f"Invalid file signature for {file_path.suffix} extension"
        )

    if findings:
        print(" Findings:")

        for finding in findings: 
            print(f" [WARNING] {finding}")

    else:
        print(" Findings: None")

    result = {
        "name": file_path.name,
        "path": str(file_path.relative_to(scan_folder)),
        "extension": file_path.suffix,
        "size": file_stats.st_size,
        "modified": modified_time,
        "accessed": accessed_time,
        "metadata_changed": changed_time,
        "sha256": file_hash,
        "detected_type": detected_type,
        "signature_valid": signature_valid,
        "findings": findings,
    }

    return result

def save_json_report(results, duplicate_groups, report_path):
    report_path.parent.mkdir(parents=True, exist_ok=True)

    files_with_findings = sum(
        1
        for result in results
        if result["findings"]
    )

    total_findings = sum(
        len(result["findings"])
        for result in results
    )

    report = {
        "summary": {
            "files_analyzed": len(results),
            "files_with_findings": files_with_findings,
            "total_findings": total_findings,
            "duplicate_groups": len(duplicate_groups),
        },
        "files": results,
        "exact_duplicates": duplicate_groups,
    }

    with open(report_path, "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=4)

    print(f"\nJSON report saved: {report_path}")

def find_exact_duplicates(results):
    hash_groups = {}

    for result in results:
        file_hash = result["sha256"]
        file_path = result["path"]

        if file_hash not in hash_groups:
            hash_groups[file_hash] = []

        hash_groups[file_hash].append(file_path)

    duplicate_groups = {}

    for file_hash, paths in hash_groups.items():
        if len(paths) > 1:
            duplicate_groups[file_hash] = paths 

    return duplicate_groups 
        

project_folder = Path(__file__).resolve().parent

print("Sleuthra - File Forensics Analyzer")
print(f"Project folder: {project_folder}")

args = parse_arguments()

scan_folder = Path(args.scan_path).expanduser().resolve()

if not scan_folder.exists():
    print(f"Error: Scan folder does not exist: {scan_folder}")
    raise SystemExit(1)

if not scan_folder.is_dir():
    print(f"Error: Scan path is not a directory: {scan_folder}")
    raise SystemExit(1)

print(f"\nScanning: {scan_folder}")

analysis_results = []

for item in sorted(scan_folder.rglob("*")):
    if item.is_file():
        result = analyze_file(item, scan_folder)
        analysis_results.append(result)

total_files = len(analysis_results)

files_with_findings = sum(
    1
    for result in analysis_results
    if result["findings"]
)

duplicate_groups = find_exact_duplicates(analysis_results)

total_findings = sum(
    len(result["findings"])
    for result in analysis_results
)

print("\nScan complete.")
print(f"Files analyzed: {total_files}")
print(f"Files with findings: {files_with_findings}")
print(f"Total findings: {total_findings}")
print(f"Duplicate groups: {len(duplicate_groups)}")

if duplicate_groups:
    print("\nExact Duplicates:")

    for file_hash, paths in duplicate_groups.items():
        print(f"\n SHA-256: {file_hash}")

        for path in paths: 
            print(f"  - {path}")
        
report_path = project_folder / "reports" / "sleuthra_report.json"

save_json_report(
    analysis_results,
    duplicate_groups,
    report_path
)

from pathlib import Path 
import hashlib 
import subprocess
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

def analyze_file(file_path):
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

    mismatch = check_extension_mismatch(file_path, detected_type)

    if mismatch:
        findings.append(
            f"Extension mismatch: {file_path.suffix} extension, "
            f"but detected as {detected_type}"
        )

    if findings:
        print(" Findings:")

        for finding in findings: 
            print(f" [WARNING] {finding}")

    else:
        print(" Findings: None")

    result = {
        "name": file_path.name,
        "extension": file_path.suffix,
        "size": file_stats.st_size,
        "modified": modified_time,
        "accessed": accessed_time,
        "metadata_changed": changed_time,
        "sha256": file_hash,
        "detected_type": detected_type,
        "findings": findings,
    }

    return result


project_folder = Path(__file__).resolve().parent

print("Sleuthra - File Forensics Analyzer")
print(f"Project folder: {project_folder}")


scan_folder = project_folder / "test_files"

if not scan_folder.exists():
    print(f"Error: Scan folder does not exist: {scan_folder}")
    raise SystemExit(1)

print(f"\nScanning: {scan_folder}")

analysis_results = []

for item in sorted(scan_folder.rglob("*")):
    if item.is_file():
        result = analyze_file(item)
        analysis_results.append(result)

total_files = len(analysis_results)

total_findings = sum(
    len(result["findings"])
    for result in analysis_results
)

print("\nScan complete.")
print(f"Files analyzed: {total_files}")
print(f"Warnings found: {total_findings}")
        


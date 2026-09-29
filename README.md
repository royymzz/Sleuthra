# Sleuthra

Sleuthra is a digital forensic file analyzer written in Python.

The project is being developed as a learning-focused digital forensics tool for inspecting files, collecting forensic metadata, verifying file integrity, and identifying potentially suspicious file characteristics.

> **Status:** Early development

## Current Features

### File Analysis

- Recursive directory scanning
- File size and filesystem timestamp collection
- SHA-256 hashing for file integrity and identification
- Content-based file type detection using the Linux `file` utility
- File-signature verification using magic bytes for PDF, JPEG, PNG, GIF, and ZIP files
- Content-based file categorization into Image, Document, Archive, Text, or Other

### Forensic Findings

- File extension/content mismatch detection
- Invalid file-signature detection for supported file types
- Structured findings for detected anomalies
- Exact duplicate detection using SHA-256 hashes

### Reporting

- Structured per-file analysis results
- JSON forensic report generation
- Relative file paths and file categories preserved in reports
- Scan summaries showing files analyzed, files with findings, total findings, and duplicate groups

### Command-Line Interface

- User-selected scan directories
- Support for relative and absolute scan paths
- Recursive analysis of nested directories
- Validation of missing or invalid scan paths
- Built-in command-line help

## Example Finding

A file may claim to be an image:

```text
fake_image.jpg
```

while content-based detection identifies it as:

```text
ASCII text
```

Sleuthra flags this discrepancy:

```text
[WARNING] Extension mismatch: .jpg extension, but detected as ASCII text
[WARNING] Invalid file signature for .jpg extension
```

This type of inconsistency can be useful during forensic file examination.

## Current Project Structure

```text
Sleuthra/
├── analyzer.py
├── README.md
├── .gitignore
└── test_files/
    ├── example.txt
    ├── fake_image.jpg
    ├── evidence/
    │   ├── nested.txt
    │   └── documents/
    │       └── deep.txt
    └── signature_tests/
        ├── valid.gif
        ├── valid.jpg
        ├── valid.pdf
        ├── valid.png
        └── valid.zip
```

The files in `test_files/` are small synthetic test samples used during development and validation.

Real forensic evidence should not be stored in the repository.

## Running Sleuthra

Sleuthra currently requires Python 3 and the Linux `file` utility.

Run the analyzer from the project directory and provide the directory to analyze:

```bash
python analyzer.py test_files
```

Sleuthra also accepts other relative or absolute directory paths:

```bash
python analyzer.py ~/Documents/evidence
```

Display command-line help with:

```bash
python analyzer.py --help
```

The selected directory is scanned recursively, including files inside nested subdirectories.

At the end of a scan, Sleuthra reports the number of files analyzed, findings detected, and exact duplicate groups. A structured JSON report is also generated in the local `reports/` directory.

## Forensic Considerations

Sleuthra reports filesystem metadata as evidence but does not assume that metadata alone proves a particular user action.

For example:

- Modification time represents the filesystem's recorded content modification time.
- Access time may be affected by filesystem mount settings and by file access during analysis.
- On Linux, `ctime` represents metadata/status change time, not file creation time.
- File extensions alone are not considered reliable indicators of actual file content.

## Development Roadmap

Planned areas of development include:

- Additional metadata extraction
- Improved file-type analysis
- Automated forensic indicators
- Evidence filtering and category-based analysis
- Improved testing and validation
- Timeline and evidence relationship analysis

The roadmap may change as the project develops.

## Disclaimer

Sleuthra is currently an educational project under active development. It is not intended to replace established professional digital forensic tools or validated forensic procedures.

## Copyright

Copyright © 2026 royymzz. All rights reserved.

No license is currently granted for copying, modifying, distributing,
or using this project's source code.

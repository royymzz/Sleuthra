# Sleuthra

Sleuthra is a digital forensic file analyzer written in Python.

The project is being developed as a learning-focused digital forensics tool for inspecting files, collecting forensic metadata, verifying file integrity, and identifying potentially suspicious file characteristics.

> **Status:** Early development

## Current Features

Sleuthra currently supports:

- File discovery within a target directory
- File extension identification
- File size collection
- SHA-256 hashing
- Content-based file type detection using the Linux `file` utility
- Detection of file extension/content mismatches
- Filesystem timestamp collection:
  - Modification time
  - Access time
  - Metadata change time
- Basic error handling for missing scan directories

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
WARNING: File extension does not match detected content!
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
    └── fake_image.jpg
```

The files in `test_files/` are small synthetic test samples used during development.

Real forensic evidence should not be stored in the repository.

## Running Sleuthra

Sleuthra currently requires Python 3 and the Linux `file` utility.

Run the analyzer from the project directory:

```bash
python analyzer.py
```

The analyzer currently scans the local `test_files` directory.

## Forensic Considerations

Sleuthra reports filesystem metadata as evidence but does not assume that metadata alone proves a particular user action.

For example:

- Modification time represents the filesystem's recorded content modification time.
- Access time may be affected by filesystem mount settings.
- On Linux, `ctime` represents metadata/status change time, not file creation time.
- File extensions alone are not considered reliable indicators of actual file content.

## Development Roadmap

Planned areas of development include:

- Structured forensic findings
- Improved directory scanning
- Structured report generation
- Additional metadata extraction
- Improved file-type analysis
- Automated forensic indicators
- Testing and validation

The roadmap may change as the project develops.

## Disclaimer

Sleuthra is currently an educational project under active development. It is not intended to replace established professional digital forensic tools or validated forensic procedures.

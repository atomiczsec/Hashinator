# Hashinator
<img src="https://github.com/atomiczsec/Hashinator/blob/main/Assets/hash.png" width="200">

Hashinator is a Python script that generates multiple hash types (MD5, SHA1, SHA256, SHA512) for files within a specified folder. It creates an interactive HTML report with comprehensive file information, advanced filtering, and sorting capabilities.

## Features

### Hash Generation
- Calculates multiple hash types:
  - MD5
  - SHA1
  - SHA256
  - SHA512
- Progress tracking for large folders
- Error handling for inaccessible files

### File Information
- File size (human-readable format: B, KB, MB, GB, TB)
- File modification date
- MIME type detection
- File type filtering

### Interactive HTML Report
- Dark/Light mode toggle
- Real-time search functionality
- File type filtering dropdown
- Sortable columns (click headers to sort)
- Copy buttons for file names and hashes
- Responsive design
- Modern UI with hover effects

## Dependencies

- Python 3.x
- `pyperclip` (for clipboard operations)
- `tqdm` (for progress bars)

Install dependencies:
```bash
pip install pyperclip tqdm
```

## Usage

1. Clone the repository or download the `hashinator.py` file
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script with various options:

   Basic usage:
   ```bash
   python hashinator.py -f /path/to/folder
   ```

   With file type filtering:
   ```bash
   python hashinator.py -f /path/to/folder -t .txt .pdf .doc
   ```

   Custom output file:
   ```bash
   python hashinator.py -f /path/to/folder -o custom_report.html
   ```

### Command Line Arguments

- `-f, --folder`: Path to the folder containing files (required)
- `-o, --output`: Output HTML file name (default: index.html)
- `-t, --types`: Filter by file types (e.g., .txt .pdf .doc)

## HTML Report Features

### Navigation and Filtering
- Search box for quick file filtering
- File type dropdown filter
- Dark/Light mode toggle
- Sortable columns

### File Information Display
- File name
- File size (human-readable)
- File type (MIME)
- Last modified date
- Multiple hash values (MD5, SHA1, SHA256, SHA512)

### Interactive Elements
- Copy buttons for file names and hashes
- Responsive table layout
- Hover effects for better UX

## Security Considerations

- Handle hash values securely
- Exercise caution when sharing or storing generated hashes
- Be mindful of file permissions when scanning directories
- Consider the security implications of clipboard operations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

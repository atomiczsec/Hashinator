# Hashinator
<img src="https://github.com/atomiczsec/Hashinator/blob/main/Assets/hash.png" width="200">

Hashinator is a Python script that generates hashes (MD5 and SHA256) for files within a specified folder. It creates an HTML report with the file names and their corresponding hashes, providing an organized view of the files' integrity.

## Features

- Calculates MD5 and SHA256 hashes for files in a folder
- Generates an HTML report with a table displaying the file names, MD5 hashes, and SHA256 hashes
- Provides buttons to copy individual MD5 and SHA256 hashes to the clipboard
- Includes a button to copy all file names to the clipboard
- Customizable CSS styles for the generated HTML report

## Dependencies

- Python 3.x
- `pyperclip` module (Install using `pip install pyperclip`)

## Usage

1. Clone the repository or download the `hashinator.py` file.
2. Open a terminal or command prompt and navigate to the project directory.
3. Install the required `pyperclip` module: `pip install pyperclip`
4. Run the script with the following command:
```
python hashinator.py -f /path/to/folder -o report.html
```

Replace `/path/to/folder` with the path to the folder containing the files you want to generate hashes for. Optionally, specify the output file name using the `-o` or `--output` argument (default is `index.html`).

5. The script will generate an HTML report named `report.html` (or the specified output file) in the current directory.
6. Open the generated HTML report in a web browser to view and interact with the file names and hashes.

## Customization

- Modify the CSS styles in the `hashinator.py` script to change the appearance of the generated HTML report, such as fonts, colors, or table styles.

## Security Considerations

- Handle hash values securely and ensure the integrity of the script and the generated HTML report.
- Exercise caution when sharing or storing the generated hashes, as they can be used for malicious purposes.

## License

This project is licensed under the [MIT License](LICENSE).


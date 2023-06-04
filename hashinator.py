import argparse
import hashlib
import os
import pyperclip

def calculate_hash(file_path, hash_algorithm):
    hash_object = hash_algorithm()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_object.update(chunk)
    return hash_object.hexdigest()

def generate_hashes(folder_path):
    hash_algorithms = {
        "md5": hashlib.md5,
        "sha256": hashlib.sha256
    }

    files_hashes = {}

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_hashes = {}
            for hash_name, hash_algorithm in hash_algorithms.items():
                file_hashes[hash_name] = calculate_hash(file_path, hash_algorithm)
            files_hashes[file_name] = file_hashes

    return files_hashes

def generate_html_file(folder_path, output_file):
    files_hashes = generate_hashes(folder_path)

    with open(output_file, "w") as html_file:
        html_file.write("<html><head><style>")
        html_file.write("body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }")
        html_file.write("table { border-collapse: collapse; width: 100%; }")
        html_file.write("th, td { text-align: left; padding: 8px; }")
        html_file.write("th { background-color: #f2f2f2; }")
        html_file.write("tr:nth-child(even) { background-color: #f2f2f2; }")
        html_file.write("tr:hover { background-color: #e2e2e2; }")
        html_file.write("button { background-color: #4CAF50; border: none; color: white; padding: 8px 16px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; }")
        html_file.write("</style></head><body>\n")
        html_file.write("<table>\n")
        html_file.write("<tr><th>File Name</th><th>MD5</th><th>SHA256</th><th></th></tr>\n")

        for file_name, file_hashes in files_hashes.items():
            md5_hash = file_hashes["md5"]
            sha256_hash = file_hashes["sha256"]
            html_file.write("<tr>")
            html_file.write(f"<td>{file_name}</td>")
            html_file.write(f"<td>{md5_hash}</td>")
            html_file.write(f"<td>{sha256_hash}</td>")
            html_file.write(f'<td><button onclick="copyToClipboard(\'{file_name}\')">Copy Filename</button> <button onclick="copyToClipboard(\'{md5_hash}\')">Copy MD5</button> <button onclick="copyToClipboard(\'{sha256_hash}\')">Copy SHA256</button></td>')
            html_file.write("</tr>\n")

        html_file.write('<tr><td><button onclick="copyAll(\'file_name\')">Copy All Filenames</button></td><td><button onclick="copyAll(\'md5\')">Copy All MD5</button></td><td><button onclick="copyAll(\'sha256\')">Copy All SHA256</button></td><td></td></tr>')
        html_file.write("</table>\n")
        html_file.write('<script>function copyToClipboard(text) { navigator.clipboard.writeText(text); }</script>')
        html_file.write('<script>function copyAll(column) { const index = column === "file_name" ? 1 : column === "md5" ? 2 : 3; const values = Array.from(document.querySelectorAll(`tr:not(:last-child) td:nth-child(${index})`)); const valuesToCopy = values.map(td => td.textContent); navigator.clipboard.writeText(valuesToCopy.join("\\n")); }</script>')
        html_file.write("</body></html>\n")

    print(f"HTML report generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Hashizor - Generate hashes of files in a folder and create an HTML report.")
    parser.add_argument("-f", "--folder", type=str, required=True, help="Path to the folder containing the files")
    parser.add_argument("-o", "--output", type=str, default="index.html", help="Output file name (default: index.html)")
    args = parser.parse_args()

    folder_path = args.folder
    output_file = args.output

    generate_html_file(folder_path, output_file)

if __name__ == "__main__":
    main()

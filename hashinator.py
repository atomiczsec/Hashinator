import argparse
import hashlib
import os
import pyperclip
from datetime import datetime
from tqdm import tqdm
import mimetypes

def calculate_hash(file_path, hash_algorithm):
    try:
        hash_object = hash_algorithm()
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_object.update(chunk)
        return hash_object.hexdigest()
    except (IOError, OSError) as e:
        return f"Error: {str(e)}"

def get_file_info(file_path):
    try:
        stats = os.stat(file_path)
        size = stats.st_size
        mod_time = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        mime_type, _ = mimetypes.guess_type(file_path)
        return {
            'size': size,
            'mod_time': mod_time,
            'mime_type': mime_type or 'Unknown'
        }
    except (IOError, OSError):
        return {
            'size': 0,
            'mod_time': 'Unknown',
            'mime_type': 'Unknown'
        }

def generate_hashes(folder_path, file_types=None):
    hash_algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }

    files_hashes = {}
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    if file_types:
        file_types = [ft.lower() for ft in file_types]
        all_files = [f for f in all_files if any(f.lower().endswith(ft) for ft in file_types)]

    for file_name in tqdm(all_files, desc="Processing files"):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_info = get_file_info(file_path)
            file_hashes = {
                'info': file_info,
                'hashes': {}
            }
            for hash_name, hash_algorithm in hash_algorithms.items():
                file_hashes['hashes'][hash_name] = calculate_hash(file_path, hash_algorithm)
            files_hashes[file_name] = file_hashes

    return files_hashes

def format_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def generate_html_file(folder_path, output_file, file_types=None):
    files_hashes = generate_hashes(folder_path, file_types)

    with open(output_file, "w") as html_file:
        html_file.write("""
<html>
<head>
    <style>
        :root { --bg-color: #ffffff; --text-color: #000000; --table-bg: #f2f2f2; --hover-color: #e2e2e2; }
        .dark-mode { --bg-color: #1a1a1a; --text-color: #ffffff; --table-bg: #2d2d2d; --hover-color: #3d3d3d; }
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: var(--bg-color); color: var(--text-color); }
        .controls { margin-bottom: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { text-align: left; padding: 8px; }
        th { background-color: var(--table-bg); cursor: pointer; }
        tr:nth-child(even) { background-color: var(--table-bg); }
        tr:hover { background-color: var(--hover-color); }
        button { background-color: #4CAF50; border: none; color: white; padding: 8px 16px; text-align: center; text-decoration: none; display: inline-block; font-size: 14px; margin: 4px 2px; cursor: pointer; }
        #searchInput { padding: 8px; margin-right: 10px; width: 200px; }
        .dark-mode-toggle { float: right; }
    </style>
</head>
<body>
    <div class="controls">
        <input type="text" id="searchInput" placeholder="Search files...">
        <button onclick="toggleDarkMode()">Toggle Dark Mode</button>
        <select id="filterType" onchange="filterTable()">
            <option value="">All Types</option>
        </select>
    </div>
    <table id="hashTable">
        <tr>
            <th onclick="sortTable(0)">File Name ↕</th>
            <th onclick="sortTable(1)">Size ↕</th>
            <th onclick="sortTable(2)">Type ↕</th>
            <th onclick="sortTable(3)">Modified ↕</th>
            <th>MD5</th>
            <th>SHA1</th>
            <th>SHA256</th>
            <th>SHA512</th>
            <th>Actions</th>
        </tr>
""")

        for file_name, file_data in files_hashes.items():
            info = file_data['info']
            hashes = file_data['hashes']
            html_file.write(f"""
        <tr>
            <td>{file_name}</td>
            <td>{format_size(info['size'])}</td>
            <td>{info['mime_type']}</td>
            <td>{info['mod_time']}</td>
            <td>{hashes['md5']}</td>
            <td>{hashes['sha1']}</td>
            <td>{hashes['sha256']}</td>
            <td>{hashes['sha512']}</td>
            <td>
                <button onclick="copyToClipboard('{file_name}')">Copy Name</button>
                <button onclick="copyToClipboard('{hashes['md5']}')">MD5</button>
                <button onclick="copyToClipboard('{hashes['sha256']}')">SHA256</button>
            </td>
        </tr>""")

        html_file.write("""
    </table>
    <script>
        function copyToClipboard(text) {
            navigator.clipboard.writeText(text);
        }

        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("hashTable");
            switching = true;
            dir = "asc";
            
            while (switching) {
                switching = false;
                rows = table.rows;
                
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    
                    if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }

        function filterTable() {
            var input = document.getElementById("searchInput");
            var filter = input.value.toLowerCase();
            var typeFilter = document.getElementById("filterType").value.toLowerCase();
            var table = document.getElementById("hashTable");
            var tr = table.getElementsByTagName("tr");

            for (var i = 1; i < tr.length; i++) {
                var td = tr[i].getElementsByTagName("td");
                var fileName = td[0].textContent.toLowerCase();
                var fileType = td[2].textContent.toLowerCase();
                
                if (fileName.indexOf(filter) > -1 && 
                    (typeFilter === "" || fileType === typeFilter)) {
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
        }

        // Populate file type filter
        window.onload = function() {
            var table = document.getElementById("hashTable");
            var types = new Set();
            var rows = table.getElementsByTagName("tr");
            
            for (var i = 1; i < rows.length; i++) {
                var type = rows[i].getElementsByTagName("td")[2].textContent;
                types.add(type);
            }
            
            var select = document.getElementById("filterType");
            types.forEach(function(type) {
                var option = document.createElement("option");
                option.value = type;
                option.text = type;
                select.appendChild(option);
            });
        }

        document.getElementById("searchInput").addEventListener("keyup", filterTable);
    </script>
</body>
</html>
""")

    print(f"HTML report generated: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Hashinator - Generate hashes of files in a folder and create an HTML report.")
    parser.add_argument("-f", "--folder", type=str, required=True, help="Path to the folder containing the files")
    parser.add_argument("-o", "--output", type=str, default="index.html", help="Output file name (default: index.html)")
    parser.add_argument("-t", "--types", type=str, nargs="+", help="Filter by file types (e.g., .txt .pdf .doc)")
    args = parser.parse_args()

    folder_path = args.folder
    output_file = args.output
    file_types = args.types

    generate_html_file(folder_path, output_file, file_types)

if __name__ == "__main__":
    main()

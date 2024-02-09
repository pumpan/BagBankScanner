import re
import tkinter as tk
from tkinter import filedialog
import json
import os

def load_settings():
    settings_path = 'settings.json'
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            return settings
    else:
        return {}

def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def get_saved_variables_folder():
    settings = load_settings()
    if 'saved_variables_path' in settings:
        return settings['saved_variables_path']
    else:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        folder_selected = filedialog.askdirectory(title="Select the SavedVariable folder")
        if folder_selected:  # If a folder was selected
            settings['saved_variables_path'] = folder_selected
            save_settings(settings)
        return folder_selected

def parse_lua_file(file_path):
    with open(file_path, 'r') as file:
        lua_content = file.read()

    combined_items = {}
    pattern = re.compile(r'\["(BagItems|BankItems)"\]\s*=\s*{\s*(.*?)\s*}', re.DOTALL)

    matches = pattern.findall(lua_content)
    for category, block in matches:
        item_pattern = re.compile(r'\["(.*?)"\]\s*=\s*(\d+),')
        item_matches = item_pattern.findall(block)
        for item, quantity in item_matches:
            match = re.match(r'\|c(.*?)\|Hitem:(\d+)[^\|]*\|h\[(.*?)\]\|h\|r', item)
            if match:
                color, item_id, name = match.groups()
                key = (name, color, item_id)
                if key in combined_items:
                    combined_items[key] += int(quantity)
                else:
                    combined_items[key] = int(quantity)

    return combined_items

def generate_html(combined_items):
    html_content = """
    <html>
    <head>
        <title>WoW Combined Items</title>
        <link rel="stylesheet" href="https://wowclassicdb.com/tooltip.min.css">
        <script>const wowdbTooltipConfig = { colorLinks: true, renameLinks: true }</script>
        <script src="https://wowclassicdb.com/tooltip.js"></script>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h2 { color: #3480af; }
            table { width: 100%; border-collapse: collapse; background-color: #1d334c; color: #ffffff; }
            th, td { border: 1px solid #ddd; padding: 8px; cursor: pointer; }
            th { background-color: #3480af; }
            input[type="text"] { margin-bottom: 10px; }
        </style>
        <script>
        function sortTable(table, column, isNumeric) {
            var tbody = table.getElementsByTagName("tbody")[0];
            var rows = Array.prototype.slice.call(tbody.getElementsByTagName("tr"));
            rows.sort(function(a, b) {
                var textA = a.cells[column].textContent.toUpperCase();
                var textB = b.cells[column].textContent.toUpperCase();
                if (isNumeric) {
                    return parseFloat(textA) - parseFloat(textB);
                } else {
                    return textA.localeCompare(textB);
                }
            });
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        }

        function searchTable(input, table) {
            var filter = input.value.toUpperCase();
            var rows = table.getElementsByTagName("tr");
            for (var i = 1; i < rows.length; i++) {
                var cells = rows[i].getElementsByTagName("td");
                var text = cells[0].textContent + cells[1].textContent;
                rows[i].style.display = text.toUpperCase().indexOf(filter) > -1 ? "" : "none";
            }
        }
        </script>
    </head>
    <body>
        <h2>Total Items</h2>
        <input type="text" onkeyup="searchTable(this, document.getElementById('totalItemsTable'))" placeholder="Search for items...">
        <table id="totalItemsTable" onclick="sortTable(this, event.target.cellIndex, event.target.cellIndex === 1)">
            <thead>
                <tr><th>Item</th><th>Total Quantity</th></tr>
            </thead>
            <tbody>
    """
    for (name, color, item_id), total_quantity in sorted(combined_items.items(), key=lambda x: x[0]):
        quality_class = {"a335ee": "q4", "0070dd": "q3", "1eff00": "q2", "ffffff": "q1", "ff8000": "q5"}.get(color[-6:], "q1")
        item_link = f"https://wowclassicdb.com/item/{item_id}"
        html_content += f'<tr><td><a class="{quality_class}" data-wowhead="item={item_id}&amp;domain=classic" href="{item_link}" target="_blank">{name}</a></td><td>{total_quantity}</td></tr>\n'

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """
    with open('wow_items.html', 'w') as html_file:
        html_file.write(html_content)
    print("HTML file generated successfully.")

# Main execution starts here
saved_variables_folder = get_saved_variables_folder()
if saved_variables_folder:
    lua_file_path = os.path.join(saved_variables_folder, 'BagBankScanner.lua')
    if os.path.exists(lua_file_path):
        combined_items = parse_lua_file(lua_file_path)
        generate_html(combined_items)
    else:
        print(f"The Lua file was not found in the selected folder: {lua_file_path}")
else:
    print("No folder selected or found. Exiting...")

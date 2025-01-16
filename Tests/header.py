# Copyright (c) 2025, Your Name
# Licensed under the MIT License. See LICENSE for details.

"""
    File to add licence information and descriptions at the beginning of each file
"""

import os

# Beispiel-Lizenz und Docstring
LICENSE = """# Copyright (c) 2025, Your Name
# Licensed under the MIT License. See LICENSE for details.
"""

DOCSTRING = '''"""
Description
"""
'''


def add_header_to_file(file_path):
    """Fügt den Lizenz- und Docstring-Header zu einer Datei hinzu, falls er noch nicht existiert."""
    with open(file_path, "r+", encoding="utf-8") as file_obj:
        content = file_obj.read()
        if LICENSE.strip() in content:
            # print(f"Header bereits in {file_path}.")
            return
        # Setzt den Dateizeiger auf den Anfang der Datei
        file_obj.seek(0, 0)
        # Schreibt Lizenz und Docstring an den Anfang der Datei
        file_obj.write(LICENSE + "\n" + DOCSTRING + "\n" + content)
        print(f"Header zu {file_path} hinzugefügt.")


if __name__ == "__main__":
    # Holen des aktuellen Arbeitsverzeichnisses (CWD)
    directory = os.getcwd()
    # Geht rekursiv durch alle Ordner und Unterordner des CWD

    for root, _, files in os.walk(directory):
        for file in files:
            # Wenn die Datei mit .py endet, füge den Header hinzu
            if file.endswith(".py"):
                add_header_to_file(os.path.join(root, file))

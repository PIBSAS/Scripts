import requests
import xml.etree.ElementTree as ET
import re

# URL del XML en GitLab
url = "https://gitlab.com/recalbox/recalbox/-/raw/master/board/recalbox/fsoverlay/recalbox/share_init/system/.emulationstation/es_bios.xml"
headers = {"User-Agent": "Mozilla/5.0"}

# Descargar XML
response = requests.get(url, headers=headers)
response.raise_for_status()
root = ET.fromstring(response.text)

# Función para normalizar nombres de variables en Bash
def sanitize_name(name):
    name = name.upper()  # Convertir a mayúsculas
    name = re.sub(r"[^\w]", "_", name)  # Reemplazar caracteres inválidos con "_"
    name = re.sub(r"_+", "_", name)  # Evitar múltiples "_"
    return name.strip("_")  # Quitar "_" extra al inicio o final

# Estructuras para los datos
systems = []
for system in root.findall("system"):
    fullname = system.get("fullname", "")
    platform = system.get("platform", "")

    path_md5_map = {}
    path_list = []  # Lista de paths para FULLNAME_PATHS

    for bios in system.findall("bios"):
        path = bios.get("path", "")
        md5 = bios.get("md5", "").replace("\n", "").replace("\r", "").replace(" ", "")  # Limpiar los espacios y saltos de línea

        if path:
            path_list.append(path)  # Agregar a FULLNAME_PATHS
            # Agregar los MD5, ya limpios de espacios
            md5s = md5.split(",")  # Los valores MD5 están separados por comas, así que los dividimos
            if path in path_md5_map:
                path_md5_map[path].extend(md5s)
            else:
                path_md5_map[path] = md5s

    systems.append({
        "fullname": fullname,
        "platform": platform,
        "path_md5_map": path_md5_map,
        "path_list": path_list
    })

# Generar script Bash
bash_script = """#!/bin/bash

# Array asociativo fullname -> platform
declare -A SYSTEMS

# Array asociativo fullname -> path
declare -A FULLNAME_PATHS
"""

for system in systems:
    fullname = system["fullname"]
    platform = system["platform"]
    sanitized_name = sanitize_name(fullname) + "_BIOS"  # Crear el nombre de variable válido en Bash

    # Agregar a SYSTEMS
    bash_script += f"\n# {fullname} ({platform})\n"
    bash_script += f"SYSTEMS['{fullname}']=\"{platform}\"\n"

    # Agregar a FULLNAME_PATHS
    path_list_str = ",".join(system["path_list"])
    bash_script += f"FULLNAME_PATHS['{fullname}']=\"{path_list_str}\"\n"

    # Declarar array asociativo con el nombre basado en fullname
    bash_script += f"declare -A {sanitized_name}\n"

    # Agregar a nuevo array BIOS
    for path, md5s in system["path_md5_map"].items():
        # Limpiar espacios extra al unir los MD5
        md5_list = ",".join(md5 for md5 in md5s)  # Los md5 ya deben estar limpios de espacios
        bash_script += f"{sanitized_name}['{path}']=\"{md5_list}\"\n"

# Guardar en un archivo .sh
with open("output.sh", "w") as f:
    f.write(bash_script)

print("✅ Script Bash generado: output.sh")

# setup_cx.py

import os
from cx_Freeze import setup, Executable

# Caminhos adicionais para garantir que os recursos sejam incluídos
additional_files = [
    ("assets/icone.ico", "assets/icone.ico"),
    ("assets/background.jpg", "assets/background.jpg"),
    ("nomes.db", "nomes.db")
]

executables = [
    Executable(
        script="main.py",
        base="Win32GUI",  # Evita o console extra
        icon="assets/icone.ico"
    )
]

setup(
    name="DestinyBot",
    version="1.0.0",
    description="Aplicação para geração de dados aleatórios com interface gráfica",
    author="vhmac",
    options={
        "build_exe": {
            "packages": ["tkinter", "Pillow", "sqlite3"],
            "include_files": additional_files,
            "include_msvcr": True,
            "path": ["."]
        }
    },
    executables=executables
)

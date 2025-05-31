import os
import sys
from cx_Freeze import setup, Executable

def listar_arquivos(pasta_base):
    arquivos = []
    for dirpath, _, filenames in os.walk(pasta_base):
        for nome in filenames:
            caminho_origem = os.path.join(dirpath, nome)
            caminho_destino = os.path.relpath(caminho_origem, ".") 
            arquivos.append((caminho_origem, caminho_destino))
    return arquivos

build_options = {
    "packages": ["pygame", "pyttsx3", "speech_recognition", "pyaudio"],
    "include_files": listar_arquivos("Recursos"),
    "include_msvcr": True
}

executavel = Executable(
    script="main.py",
    base="Win32GUI" if sys.platform == "win32" else None,
    target_name="PorquinhoGame.exe",
    icon="Recursos/icone.ico"
)

setup(
    name="Porquinho Caçador de Moedas",
    version="1.0",
    description="Jogo desenvolvido por Kaiki André Pauletto",
    options={"build_exe": build_options},
    executables=[executavel]
)

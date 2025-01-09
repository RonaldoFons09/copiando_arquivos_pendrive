import os
import shutil
from pathlib import Path
import psutil  # Biblioteca para verificar dispositivos conectados


# Obtém os caminhos das pastas padrão do Windows
def obter_pastas_padrao():
    user_home = Path.home()
    pastas = {
        "Área de Trabalho": user_home / "Desktop",
        "Imagens": user_home / "Pictures",
        "Vídeos": user_home / "Videos",
        "Documentos": user_home / "Documents",
        "Downloads": user_home / "Downloads",
        "Músicas": user_home / "Music",
    }
    return pastas


# Função para identificar automaticamente o pen drive
def detectar_pen_drive():
    for particao in psutil.disk_partitions():
        if "removable" in particao.opts:  # Verifica se é um dispositivo removível
            return particao.mountpoint  # Retorna o caminho do pen drive
    return None


# Extensões de arquivos para copiar
extensoes = (".pdf", ".jpg", ".jpeg", ".png", ".avi", ".mkv", ".docx", ".mp3")


# Função para copiar arquivos
def copiar_arquivos(origem, destino, extensoes):
    if not os.path.exists(destino):
        print(f"Criando pasta no pen drive: {destino}")
        os.makedirs(destino)

    for root, dirs, files in os.walk(origem):
        for file in files:
            if file.lower().endswith(extensoes):
                arquivo_origem = os.path.join(root, file)
                arquivo_destino = os.path.join(destino, file)

                try:
                    print(f"Copiando: {arquivo_origem} -> {arquivo_destino}")
                    shutil.copy2(arquivo_origem, arquivo_destino)
                except Exception as e:
                    print(f"Erro ao copiar {file}: {e}")


# Detecta automaticamente o pen drive
pen_drive = detectar_pen_drive()

if pen_drive:
    print(f"Pen drive detectado: {pen_drive}")

    # Obtém as pastas padrão e copia os arquivos
    pastas = obter_pastas_padrao()
    for nome_pasta, caminho_pasta in pastas.items():
        if caminho_pasta.exists():
            print(f"\nPercorrendo a pasta {nome_pasta}...")
            destino_pasta = os.path.join(pen_drive, nome_pasta)
            copiar_arquivos(caminho_pasta, destino_pasta, extensoes)

    print("\nCópia concluída!")
else:
    print("Nenhum pen drive detectado. Conecte um pen drive e tente novamente.")

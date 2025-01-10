import os
import ctypes  # Necessário para alterar atributos de arquivos no Windows


# Constantes de atributos de arquivo no Windows
FILE_ATTRIBUTE_HIDDEN = 0x02
FILE_ATTRIBUTE_NORMAL = 0x80


# Remove o atributo de oculto de um arquivo ou pasta
def tornar_visivel(caminho):
    try:
        # Define o atributo como "normal", removendo o oculto
        ctypes.windll.kernel32.SetFileAttributesW(caminho, FILE_ATTRIBUTE_NORMAL)
        print(f"Agora visível: {caminho}")
    except Exception as e:
        print(f"Erro ao tornar visível {caminho}: {e}")


# Tornar todos os arquivos e pastas visíveis em um diretório
def tornar_tudo_visivel(diretorio):
    if not os.path.exists(diretorio):
        print(f"O diretório {diretorio} não existe.")
        return

    for root, dirs, files in os.walk(diretorio):
        for nome in dirs:
            caminho_pasta = os.path.join(root, nome)
            tornar_visivel(caminho_pasta)  # Torna pastas visíveis
        for nome in files:
            caminho_arquivo = os.path.join(root, nome)
            tornar_visivel(caminho_arquivo)  # Torna arquivos visíveis

    print(f"\nTodos os arquivos e pastas em '{diretorio}' agora estão visíveis.")


# Detecta automaticamente o pen drive (ou insira o caminho manualmente)
def detectar_pen_drive():
    import psutil  # Biblioteca para verificar dispositivos conectados

    for particao in psutil.disk_partitions():
        if "removable" in particao.opts:  # Verifica se é um dispositivo removível
            return particao.mountpoint  # Retorna o caminho do pen drive
    return None


# Código principal
pen_drive = detectar_pen_drive()

if pen_drive:
    print(f"Pen drive detectado: {pen_drive}")
    print("\nTornando todos os arquivos e pastas visíveis...")
    tornar_tudo_visivel(pen_drive)
else:
    print("Nenhum pen drive detectado. Conecte um pen drive e tente novamente.")

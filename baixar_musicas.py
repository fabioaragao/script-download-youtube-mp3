import os
import sys
import platform
import subprocess

# === 1. Define diretório de trabalho como o diretório do script ===
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"📁 Diretório de trabalho: {os.getcwd()}")

# === 2. Verifica e carrega lista de músicas ===
list_file = 'music_list.txt'
if not os.path.isfile(list_file):
    print(f"❌ Arquivo '{list_file}' não encontrado.")
    sys.exit(1)

with open(list_file, 'r', encoding='utf-8') as f:
    musicas = [line.strip() for line in f if line.strip()]

print(f"\n🎶 {len(musicas)} músicas carregadas de '{list_file}'.\n")

# === 3. Detecta o SO ===
so = platform.system()
print(f"💻 Sistema operacional: {so}")

# === 4. Instala dependências Python ===
def instalar_pacote(pacote):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        print(f"✅ Pacote '{pacote}' instalado com sucesso.")
    except subprocess.CalledProcessError:
        print(f"❌ Falha ao instalar o pacote '{pacote}'.")
        sys.exit(1)

for pacote in ("yt-dlp", "youtubesearchpython"):
    try:
        __import__(pacote.replace("-", "_"))
    except ImportError:
        print(f"📦 Instalando '{pacote}'...")
        instalar_pacote(pacote)

# === 5. Instala ffmpeg ===
def instalar_ffmpeg_linux():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("🎬 ffmpeg já está instalado.")
    except:
        print("🔧 Instalando ffmpeg no Linux...")
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
        print("✅ ffmpeg instalado.")

def instalar_ffmpeg_windows():
    ffmpeg_dir = os.path.join(script_dir, "ffmpeg")
    if not os.path.isdir(ffmpeg_dir):
        import urllib.request, zipfile, io
        print("🔽 Baixando ffmpeg para Windows...")
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        data = urllib.request.urlopen(url).read()
        with zipfile.ZipFile(io.BytesIO(data)) as zip_ref:
            zip_ref.extractall(ffmpeg_dir)
        print("✅ ffmpeg extraído.")
    bin_path = None
    for root, dirs, files in os.walk(ffmpeg_dir):
        if "ffmpeg.exe" in files:
            bin_path = root
            break
    if bin_path:
        os.environ["PATH"] += os.pathsep + bin_path
        print(f"🛠️ PATH atualizado com ffmpeg: {bin_path}")
    else:
        print("❌ Não foi possível localizar ffmpeg.exe.")
        sys.exit(1)

if so == "Linux":
    instalar_ffmpeg_linux()
elif so == "Windows":
    instalar_ffmpeg_windows()
else:
    print("❌ Sistema operacional não suportado.")
    sys.exit(1)

# === 6. Importa bibliotecas ===
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
import time

# === 7. Configurações do yt-dlp ===
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}

# === 8. Função de download ===
def baixar_musica(titulo, index, total):
    print(f"🔎 [{index}/{total}] Procurando por: {titulo}")
    try:
        videos = VideosSearch(titulo, limit=1).result().get('result', [])
        if not videos:
            print(f"❌ Nenhum vídeo encontrado para: {titulo}")
            return
        url = videos[0]['link']
        print(f"✅ Encontrado! Iniciando download de: {videos[0]['title']}")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"🎉 Concluído: {titulo}\n")
    except Exception as e:
        print(f"❌ Erro ao baixar '{titulo}': {e}\n")

# === 9. Inicia processo ===
print("🚀 Iniciando processo de download...\n")

for i, musica in enumerate(musicas, 1):
    baixar_musica(musica, i, len(musicas))
    if i < len(musicas):
        print("➡️ Indo para a próxima música...\n")
        time.sleep(1)  # intervalo entre downloads (opcional)

print("✅ Todos os downloads foram processados!")

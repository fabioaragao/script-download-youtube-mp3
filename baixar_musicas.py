import os
import sys
import platform
import subprocess
import time
import logging

# === 1. Configuração de Logging ===
# Define diretório de trabalho como o diretório do script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

log_file = os.path.join(script_dir, 'download_log.txt')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info(f"📁 Diretório de trabalho: {os.getcwd()}")

# === 2. Verifica e carrega lista de músicas ===
list_file = 'music_list.txt'
if not os.path.isfile(list_file):
    logging.error(f"❌ Arquivo '{list_file}' não encontrado.")
    sys.exit(1)

with open(list_file, 'r', encoding='utf-8') as f:
    musicas = [line.strip() for line in f if line.strip()]

logging.info(f"🎶 {len(musicas)} músicas carregadas de '{list_file}'.")

# === 3. Detecta o SO ===
so = platform.system()
logging.info(f"💻 Sistema operacional: {so}")

# === 4. Instala dependências Python (Apenas yt-dlp) ===
def instalar_pacote(pacote):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pacote])
        logging.info(f"✅ Pacote '{pacote}' instalado com sucesso.")
    except subprocess.CalledProcessError:
        logging.error(f"❌ Falha ao instalar o pacote '{pacote}'.")
        sys.exit(1)

# Removemos youtubesearchpython pois o yt-dlp fará a busca
pacotes_necessarios = ["yt-dlp"]

for pacote in pacotes_necessarios:
    try:
        # Tenta importar o módulo (substituindo hifens por underscores)
        __import__(pacote.replace("-", "_"))
    except ImportError:
        logging.info(f"📦 Instalando '{pacote}'...")
        instalar_pacote(pacote)

# === 5. Instala ffmpeg ===
def instalar_ffmpeg_linux():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        logging.info("🎬 ffmpeg já está instalado.")
    except:
        logging.info("🔧 Instalando ffmpeg no Linux...")
        try:
            subprocess.check_call(["sudo", "apt", "update"])
            subprocess.check_call(["sudo", "apt", "install", "-y", "ffmpeg"])
            logging.info("✅ ffmpeg instalado.")
        except subprocess.CalledProcessError as e:
            logging.error(f"❌ Erro ao instalar ffmpeg: {e}")

def instalar_ffmpeg_windows():
    ffmpeg_dir = os.path.join(script_dir, "ffmpeg")
    # Verifica se o ffmpeg já está configurado (pode estar no PATH ou na pasta)
    
    # Tenta achar no path atual primeiro
    bin_path = None
    if os.path.isdir(ffmpeg_dir):
        for root, dirs, files in os.walk(ffmpeg_dir):
            if "ffmpeg.exe" in files:
                bin_path = root
                break
    
    if bin_path:
        os.environ["PATH"] += os.pathsep + bin_path
        logging.info(f"🛠️ PATH atualizado com ffmpeg local: {bin_path}")
        return

    # Se não achou, checa se já existe no sistema
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        logging.info("🎬 ffmpeg detectado no sistema.")
        return
    except FileNotFoundError:
        pass

    # Se chegou aqui, precisa instalar/baixar
    if not os.path.isdir(ffmpeg_dir):
        import urllib.request, zipfile, io
        logging.info("🔽 Baixando ffmpeg para Windows...")
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        try:
            req = urllib.request.urlopen(url)
            data = req.read()
            with zipfile.ZipFile(io.BytesIO(data)) as zip_ref:
                zip_ref.extractall(ffmpeg_dir)
            logging.info("✅ ffmpeg extraído.")
        except Exception as e:
            logging.error(f"❌ Erro ao baixar ffmpeg: {e}")
            sys.exit(1)
            
    # Procura novamente o binário
    for root, dirs, files in os.walk(ffmpeg_dir):
        if "ffmpeg.exe" in files:
            bin_path = root
            break
            
    if bin_path:
        os.environ["PATH"] += os.pathsep + bin_path
        logging.info(f"🛠️ PATH atualizado com ffmpeg recém-baixado: {bin_path}")
    else:
        logging.error("❌ Não foi possível localizar ffmpeg.exe após download.")
        sys.exit(1)

if so == "Linux":
    instalar_ffmpeg_linux()
elif so == "Windows":
    instalar_ffmpeg_windows()
else:
    logging.error("❌ Sistema operacional não suportado.")
    sys.exit(1)

# === 6. Configurações do yt-dlp e Importação ===
# Importa APÓS garantir que está instalado
try:
    from yt_dlp import YoutubeDL
except ImportError:
    logging.error("❌ Erro crítico: yt-dlp não pôde ser importado mesmo após tentativa de instalação.")
    sys.exit(1)

# Configurações para buscar e baixar
# ytsearch1: termo -> busca 1 resultado e baixa
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
    'default_search': 'ytsearch1', # Habilita busca automática
}

# === 8. Função de download ===
def baixar_musica(termo_busca, index, total):
    logging.info(f"🔎 [{index}/{total}] Buscando e baixando: {termo_busca}")
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            # extract_info com download=True faz tudo de uma vez
            # Se a string não for URL, o default_search='ytsearch1' cuida disso
            info = ydl.extract_info(termo_busca, download=True)
            
            # Se for uma pesquisa, info['entries'][0] contém os dados
            if 'entries' in info:
                video_info = info['entries'][0]
            else:
                video_info = info
                
            titulo_video = video_info.get('title', 'Desconhecido')
            logging.info(f"✅ Vídeo encontrado: {titulo_video}")
            
            # Tentar adivinhar o nome do arquivo final
            # O yt-dlp pode mudar o nome levemente dependendo dos caracteres
            expected_filename = ydl.prepare_filename(video_info)
            # Como convertemos para mp3, a extensão muda de .webm/.m4a para .mp3
            pre_ext = os.path.splitext(expected_filename)[0]
            final_filename = f"{pre_ext}.mp3"
            
            # Validação simples
            if os.path.exists(final_filename):
                size = os.path.getsize(final_filename)
                if size > 0:
                     logging.info(f"🎉 Sucesso: '{final_filename}' salvo ({size/1024/1024:.2f} MB).")
                else:
                     logging.error(f"⚠️ Atenção: O arquivo '{final_filename}' foi criado mas está vazio.")
            else:
                # Às vezes o yt-dlp limpa caracteres especiais, então pode ser difícil achar o arquivo exato
                # Mas se não deu erro no download, provavelmente está lá.
                logging.warning(f"⚠️ Download finalizado, mas não consegui verificar o arquivo exato '{final_filename}'. Verifique a pasta.")
                
    except Exception as e:
        logging.error(f"❌ Erro ao processar '{termo_busca}': {str(e)}")

# === 9. Inicia processo ===
logging.info("🚀 Iniciando fila de downloads...\n")

for i, musica in enumerate(musicas, 1):
    baixar_musica(musica, i, len(musicas))
    if i < len(musicas):
        logging.info("➡️ Aguardando para próxima música...")
        time.sleep(1) 

logging.info("\n✅ Processo finalizado! Verifique o arquivo 'download_log.txt' para detalhes.")

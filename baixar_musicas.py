import os
import sys
import platform
import subprocess
import time
import logging
import unicodedata
import re

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
def normalize_string(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.replace('–', '-').replace('—', '-').replace('’', "'").replace('‘', "'")
    s = re.sub(r"[^0-9A-Za-z\s]", ' ', s)
    s = re.sub(r"\s+", ' ', s).strip().lower()
    return s


def sanitize_filename(name: str) -> str:
    name = unicodedata.normalize('NFC', name)
    invalid = '<>:"/\\|?*'
    sanitized = ''.join('_' if c in invalid else c for c in name)
    sanitized = ''.join(ch for ch in sanitized if ord(ch) >= 32)
    sanitized = ' '.join(sanitized.split()).strip()
    return sanitized or 'downloaded_audio'


def baixar_musica(termo_busca, index, total):
    # Espaçamento extra no log para separar cada música
    logging.info(f"\n\n🔎 [{index}/{total}] Buscando e baixando: {termo_busca}")

    try:
        # Detecta se a entrada é uma URL do YouTube
        is_url = False
        term_lower = termo_busca.lower()
        if term_lower.startswith('http://') or term_lower.startswith('https://') or 'youtube.com' in term_lower or 'youtu.be' in term_lower:
            is_url = True

        if is_url:
            video_url = termo_busca
            video_title = None

            # Tenta obter informações do vídeo para extrair o título
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=False)
                    video_title = info.get('title') if info else None
            except Exception:
                logging.warning(f"⚠️ Falha ao obter metadados para URL '{video_url}', tentando download direto.")

            video_title = video_title or video_url
            logging.info(f"🔗 URL detectada. Baixando: {video_url}")

            safe_title = sanitize_filename(video_title)
            ydl_opts_local = dict(ydl_opts)
            ydl_opts_local['outtmpl'] = f"{safe_title}.%(ext)s"

            pp = list(ydl_opts_local.get('postprocessors', []))
            if not any(p.get('key') == 'FFmpegMetadata' for p in pp):
                pp.append({'key': 'FFmpegMetadata'})
            ydl_opts_local['postprocessors'] = pp

            with YoutubeDL(ydl_opts_local) as ydl_local:
                ydl_local.extract_info(video_url, download=True)

            final_filename = f"{safe_title}.mp3"
            if os.path.exists(final_filename):
                size = os.path.getsize(final_filename)
                if size > 0:
                    logging.info(f"🎉 Sucesso: '{final_filename}' salvo ({size/1024/1024:.2f} MB).")
                    return True
                else:
                    logging.error(f"⚠️ Atenção: O arquivo '{final_filename}' foi criado mas está vazio.")
                    return False
            else:
                logging.warning(f"⚠️ Download finalizado, mas não consegui verificar o arquivo exato '{final_filename}'. Verifique a pasta.")
                return False

        # Se não for URL, mantém a lógica de busca por título
        search_query = f"ytsearch10:{termo_busca}"

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            entries = info.get('entries', []) if info else []
            matched_entry = None

            termo_norm = normalize_string(termo_busca)

            for entry in entries:
                title = entry.get('title') if entry else ''
                title_norm = normalize_string(title)
                if title_norm == termo_norm or termo_norm in title_norm or title_norm in termo_norm:
                    matched_entry = entry
                    break

            if not matched_entry:
                logging.warning(f"⚠️ Não foi encontrado resultado com título parecido para: '{termo_busca}'. Pulando.")
                return False

            video_url = matched_entry.get('webpage_url') or f"https://www.youtube.com/watch?v={matched_entry.get('id')}"
            video_title = matched_entry.get('title') or termo_busca
            logging.info(f"✅ Título localizado: {video_title}. Baixando {video_url} ...")

            safe_title = sanitize_filename(video_title)
            ydl_opts_local = dict(ydl_opts)
            ydl_opts_local['outtmpl'] = f"{safe_title}.%(ext)s"

            pp = list(ydl_opts_local.get('postprocessors', []))
            if not any(p.get('key') == 'FFmpegMetadata' for p in pp):
                pp.append({'key': 'FFmpegMetadata'})
            ydl_opts_local['postprocessors'] = pp

            with YoutubeDL(ydl_opts_local) as ydl_local:
                ydl_local.extract_info(video_url, download=True)

            final_filename = f"{safe_title}.mp3"
            if os.path.exists(final_filename):
                size = os.path.getsize(final_filename)
                if size > 0:
                    logging.info(f"🎉 Sucesso: '{final_filename}' salvo ({size/1024/1024:.2f} MB).")
                    return True
                else:
                    logging.error(f"⚠️ Atenção: O arquivo '{final_filename}' foi criado mas está vazio.")
                    return False
            else:
                logging.warning(f"⚠️ Download finalizado, mas não consegui verificar o arquivo exato '{final_filename}'. Verifique a pasta.")
                return False

    except Exception as e:
        logging.error(f"❌ Erro ao processar '{termo_busca}': {str(e)}")
        return False

# === 9. Inicia processo ===
logging.info("🚀 Iniciando fila de downloads...\n")

# Contadores de resultados e listas de relatório
musicas_encontradas = 0
musicas_nao_encontradas = 0
musicas_falharam = []
musicas_sucesso = []

for i, musica in enumerate(musicas, 1):
    # Chama o downloader (o próprio imprime espaçamento no log)
    sucesso = baixar_musica(musica, i, len(musicas))
    if sucesso:
        musicas_encontradas += 1
        musicas_sucesso.append(musica)
        logging.info(f"✅ Resultado: '{musica}' baixada com sucesso.")
    else:
        musicas_nao_encontradas += 1
        musicas_falharam.append(musica)
        logging.warning(f"❌ Resultado: não foi possível baixar: '{musica}'")

    # Pequena pausa e separador para o próximo item
    if i < len(musicas):
        logging.info("➡️ Aguardando para próxima música...\n")
        time.sleep(1)

logging.info(f"\n📊 Resumo: {musicas_encontradas} baixadas, {musicas_nao_encontradas} falharam.")

if musicas_falharam:
    logging.info("\n🎯 Lista de músicas NÃO baixadas:")
    for idx, m in enumerate(musicas_falharam, 1):
        logging.info(f"  {idx}. {m}")
    logging.info("\nVerifique os motivos acima e tente novamente para essas entradas.")
else:
    logging.info("\n🎉 Todas as músicas foram baixadas com sucesso.")

logging.info("\n✅ Processo finalizado! Verifique o arquivo 'download_log.txt' para detalhes.")

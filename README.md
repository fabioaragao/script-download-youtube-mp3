# Music Downloader via YouTube Search

Este projeto contém um script Python que lê uma lista de músicas de um arquivo `.txt`, busca cada música no YouTube, e faz o download do áudio em formato `.mp3`. O processo é feito **uma música por vez**, com mensagens verbosas para acompanhamento do status de cada etapa.

---

## Funcionalidades

- Lê uma lista de músicas do arquivo `music_list.txt` (uma música por linha).
- Detecta automaticamente o sistema operacional (Windows ou Linux).
- Instala automaticamente as dependências Python necessárias (`yt-dlp` e `youtubesearchpython`).
- Detecta se o `ffmpeg` está instalado; caso contrário, instala (Linux) ou usa o executável fornecido (Windows).
- Procura a melhor correspondência da música no YouTube.
- Faz download do áudio da música em alta qualidade e converte para `.mp3`.
- Processo sequencial, uma música por vez, com mensagens claras de sucesso, falha, ou progresso.
- Fácil de usar e configurar.

---

## Requisitos

- **Python 3.7+** instalado no sistema.
- Internet ativa para baixar dependências e músicas.
- No Linux, privilégios para instalar `ffmpeg` via apt (ou já ter instalado).
- No Windows, o executável do `ffmpeg` já está incluído na pasta `/ffmpeg` para facilitar (não precisa instalar nada extra).

---

## Estrutura do Projeto
/
├── baixar_musicas.py # Script principal para rodar os downloads
├── music_list.txt # Lista de músicas (uma por linha)
├── ffmpeg/ # Pasta contendo executável ffmpeg para Windows
└── README.md # Este arquivo


---

## Como usar

### 1. Preparar lista de músicas

Crie o arquivo `music_list.txt` no mesmo diretório do script. Exemplo:
Cafe 432 ft Janine Dyer - Freedom (Cafe 432 Extended Rework Mix)
Michael Gray ft Leela D - Save Me
Staxx - Joy (Dr Packer Extended Mix)


Cada linha é uma busca independente no YouTube.

### 2. Rodar o script

No terminal (Linux/macOS) ou Prompt de Comando/PowerShell (Windows), execute:

```bash
python baixar_musicas.py


O script fará o resto: instalará dependências, verificará o ffmpeg, buscará e baixará cada música, exibindo mensagens detalhadas.
3. Resultado

Ao final, os arquivos .mp3 estarão salvos no mesmo diretório.

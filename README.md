# Music Downloader via YouTube

Script Python que lê uma lista (`music_list.txt`) e baixa o áudio em MP3 a partir do YouTube.

## O que o script faz

- Lê cada linha de `music_list.txt` (uma entrada por linha).
- Se a linha for uma URL do YouTube (ex.: `https://www.youtube.com/watch?v=...` ou `https://youtu.be/...`), o script baixa diretamente esse vídeo.
- Se a linha for um nome de música/artista, o script busca no YouTube e só baixa quando encontra um título exatamente igual ao termo (comparação case-insensitive e com normalização de espaços/accentos).
- Converte para MP3 (192 kbps) usando `ffmpeg` e salva arquivos na mesma pasta do script.
- Gera `download_log.txt` com detalhes de cada operação e, ao final, os totais:
  - `musicas encontradas: X`
  - `musicas nao encontradas: X`

## Requisitos

- Python 3.7+
- Conexão com internet
- `yt-dlp` será instalado automaticamente pelo script se ausente
- `ffmpeg` deve estar disponível; o script tenta detectar/baixar/configurar no Windows e instalar via `apt` no Linux quando possível

## Como usar

1. Edite (ou crie) `music_list.txt` no mesmo diretório do script.

   Exemplos de linhas válidas:

   - Nome (busca por título exato):

     Cafe 432 ft Janine Dyer - Freedom
     Michael Gray - Save Me

   - URL direta do vídeo (o script baixa este vídeo):

     https://www.youtube.com/watch?v=xxxxxxxxxxx
     https://youtu.be/xxxxxxxxxxx

2. Execute o script:

PowerShell (Windows):

```powershell
python baixar_musicas.py
```

Bash (Linux/macOS):

```bash
python3 baixar_musicas.py
```

O script fará:
- Instalação do `yt-dlp` (se necessário).
- Verificação/instalação do `ffmpeg` quando aplicável.
- Processamento de cada entrada do `music_list.txt`.
- Geração do log em `download_log.txt`.

## Resultado

- Arquivos `.mp3` salvos na mesma pasta do script (nomes sanitizados).
- Consulte `download_log.txt` para ver status de cada item e os totais de encontrados/nao encontrados.

## Observações

- A busca por nome exige título exatamente igual (após normalizações). Se o vídeo postado tiver título diferente, use a URL na lista para garantir que o vídeo correto seja baixado.
- Caso queira suporte para buscas mais flexíveis (fuzzy/parte do título), eu posso adicionar essa opção.

---

Se quiser, atualizo o README com instruções adicionais (ex.: exemplos de `music_list.txt`, flags de execução, ou como instalar dependências manualmente).

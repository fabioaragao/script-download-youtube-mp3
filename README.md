# Music Downloader via YouTube Search

Este projeto contém um script Python que lê uma lista de músicas de um arquivo `.txt`, busca cada música no YouTube automaticamente, e faz o download do áudio em formato `.mp3`.

---

## Funcionalidades

- **Busca Automática**: Lê `music_list.txt` e encontra a melhor correspondência no YouTube.
- **Download em MP3**: Baixa e converte o áudio automaticamente com alta qualidade (192kbps).
- **Sistema de Logs**: Gera um arquivo `download_log.txt` com detalhes de cada operação (sucessos, erros, avisos e caminhos dos arquivos).
- **Validação Automática**: Verifica se o arquivo foi realmente criado e se não está vazio após o download.
- **Multi-plataforma**: Funciona em Windows e Linux, com detecção automática.
- **Gestão de Dependências**: Instala automaticamente o `yt-dlp` e tenta configurar o `ffmpeg` se não estivar presente.

---

## Requisitos

- **Python 3.7+** instalado.
- Conexão com internet.
- **Windows**: O script tenta baixar o `ffmpeg` automaticamente se não encontrar no sistema ou na pasta local `ffmpeg/`.
- **Linux**: Tenta instalar via `sudo apt install ffmpeg` se necessário.

---

## Como usar

### 1. Preparar lista de músicas

Crie (ou edite) o arquivo `music_list.txt` no mesmo diretório do script. Coloque o nome da música/artista por linha.
Exemplo:
```text
Cafe 432 ft Janine Dyer - Freedom
Michael Gray - Save Me
Staxx - Joy
```

### 2. Rodar o script

No terminal ou Prompt de Comando, execute:

```bash
python baixar_musicas.py
```

O script irá:
1. Instalar a biblioteca `yt-dlp` se não estiver instalada.
2. Verificar se o `ffmpeg` está acessível (instalando ou baixando se preciso).
3. Buscar cada termo no YouTube e baixar o primeiro resultado.
4. Salvar o log de execução em `download_log.txt`.

### 3. Resultado

- Os arquivos `.mp3` serão salvos na mesma pasta do script.
- Abra o arquivo `download_log.txt` para conferir o status de cada download.

---

## Detalhes Técnicos

- **Mecanismo Principal**: Utiliza `yt-dlp` tanto para a busca (`ytsearch1`) quanto para o download e pós-processamento de áudio.
- **Dependências**: Removeu-se a dependência de `youtubesearchpython` para maior estabilidade.
- **Log**: Utiliza o módulo `logging` do Python com encoding UTF-8.

---

## Contribuição

Sinta-se livre para modificar e melhorar!

# Music Downloader via YouTube Search

Este projeto contém um script Python que lê uma lista de músicas de um arquivo `.txt`, busca cada música no YouTube, e faz o download do áudio em formato `.mp3`. O processo é feito **uma música por vez**, com mensagens verbosas para acompanhamento do status de cada etapa.

---

## Funcionalidades

- Lê uma lista de músicas do arquivo `music_list.txt` (uma música por linha).
- Detecta automaticamente o sistema operacional (Windows ou Linux).
- Instala automaticamente as dependências Python necessárias (`yt-dlp` e `youtubesearchpython`).
- Detecta se o `ffmpeg` está instalado; caso contrário, instala (Linux) ou usa o executável fornecido (Windows).
- Se estiver no Windows e não houver o ffmpeg, você pode baixar manualmente através do link que está no arquivo `link_para_baixar_o_ffmpeg.txt`.
- Procura a melhor correspondência da música no YouTube.
- Faz download do áudio da música em alta qualidade e converte para `.mp3`.
- Processo sequencial, uma música por vez, com mensagens claras de sucesso, falha, ou progresso.
- Fácil de usar e configurar.

---

## Requisitos

- **Python 3.7+** instalado no sistema.
- Internet ativa para baixar dependências e músicas.
- No Linux, privilégios para instalar `ffmpeg` via apt (ou já ter instalado).
- No Windows, caso não queira instalar manualmente, o link para baixar o `ffmpeg` está no arquivo `link_para_baixar_o_ffmpeg.txt`.

---


## Como usar

### 1. Preparar lista de músicas

Crie o arquivo `music_list.txt` no mesmo diretório do script. Exemplo:
Cafe 432 ft Janine Dyer - Freedom (Cafe 432 Extended Rework Mix)
Michael Gray ft Leela D - Save Me
Staxx - Joy (Dr Packer Extended Mix)

---


Cada linha é uma busca independente no YouTube.

### 2. Instalar ffmpeg (somente Windows)

- Caso esteja usando Windows e não tenha o `ffmpeg` instalado, baixe utilizando o link 
disponível no arquivo `link_para_baixar_o_ffmpeg.txt`.
- Após baixar, extraia e coloque o executável `ffmpeg.exe` no mesmo diretório do 
script **ou** adicione o caminho do ffmpeg nas variáveis de ambiente do Windows.

### 3. Rodar o script

No terminal (Linux/macOS) ou Prompt de Comando/PowerShell (Windows), execute:

```bash
python baixar_musicas.py

O script fará o resto: instalará dependências, verificará o ffmpeg, buscará e baixará cada música, exibindo mensagens detalhadas.
4. Resultado

Ao final, os arquivos .mp3 estarão salvos no mesmo diretório.


Detalhes Técnicos

    Usa yt-dlp para download e conversão.

    Usa youtubesearchpython para busca.

    No Linux, tenta instalar ffmpeg via apt se não estiver instalado.

    No Windows, utiliza o executável ffmpeg.exe caso esteja no diretório ou no PATH.

Considerações

    O download depende da disponibilidade dos vídeos no YouTube.

    Respeite os termos de uso do YouTube e direitos autorais.

    Em caso de falha na busca ou no download, o script reporta o erro e segue para a próxima música.

    Para melhorar performance ou adicionar funcionalidades (ex: paralelismo), você pode modificar o script.

Contribuição

Pull requests e issues são bem-vindos!
Licença

Este projeto está sob a licença MIT — sinta-se livre para usar e modificar.
Contato

Caso tenha dúvidas ou sugestões, abra uma issue ou me contate.

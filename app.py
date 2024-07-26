from flask import Flask, render_template, request, send_file  # Importa as funções necessárias do Flask
import yt_dlp  # Importa o yt-dlp para download de vídeos do YouTube
import os  # Importa a biblioteca os para manipulação de arquivos e diretórios

# Cria uma instância da aplicação Flask
app = Flask(__name__)

# Define a rota principal da aplicação
@app.route('/')
def index():
    # Renderiza e retorna o template 'index.html'
    return render_template('index.html')

# Define a rota para o download de arquivos
@app.route('/downloads', methods=['POST'])  # Permite apenas requisições POST
def download():
    # Obtém a URL e o formato selecionado do formulário enviado
    url = request.form['url']
    format_choice = request.form['format']

    # Configura as opções para o yt-dlp com base no formato escolhido
    if format_choice == 'mp3':
        ydl_opts = {
            'format': 'bestaudio/best',  # Seleciona o melhor áudio disponível
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Define o caminho de saída do arquivo
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Usa FFmpeg para extrair o áudio
                'preferredcodec': 'mp3',  # Define o codec preferido como MP3
                'preferredquality': '192',  # Define a qualidade do áudio
            }],
        }
    elif format_choice == 'mp4':
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',  # Seleciona o melhor vídeo e áudio disponíveis
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Define o caminho de saída do arquivo
            'merge_output_format': 'mp4',  # Define o formato de saída como MP4
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',  # Usa FFmpeg para converter o vídeo
                'preferedformat': 'mp4',  # Define o formato preferido como MP4
            }],
            'postprocessor_args': [
                '-c:a', 'aac',  # Define o codec de áudio como AAC
                '-b:a', '192k'  # Define a taxa de bits do áudio para 192k
            ],
        }

    # Cria uma instância do yt-dlp com as opções configuradas
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)  # Extrai informações do vídeo e realiza o download
        # Prepara o caminho do arquivo baixado com a extensão correta
        if format_choice == 'mp3':
            file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        elif format_choice == 'mp4':
            file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp4').replace('.mkv', '.mp4')

    # Envia o arquivo baixado como um anexo para o usuário
    return send_file(file_path, as_attachment=True)

# Executa a aplicação Flask
if __name__ == '__main__':
    # Verifica se o diretório 'downloads' existe; se não, cria um
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(debug=True)  # Inicia o servidor Flask em modo de depuração

import os
from app import app  # Substitua "app" pelo nome do seu arquivo principal se for diferente

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000)  # Permite acesso externo

import os
from pytube import Search
import yt_dlp as youtube_dl
import logging

pytube_logger = logging.getLogger('pytube')
pytube_logger.setLevel(logging.ERROR)

def search_youtube(query):
    """Busca vídeos no YouTube utilizando pytube e retorna o URL do primeiro resultado."""
    try:
        search = Search(query)
        results = search.results
        if results:
            return results[0].watch_url
        else:
            return None
    except Exception as e:
        print(f"Erro na busca do YouTube para '{query}': {e}")
        return None

def download_audio(url, download_path):
    """Baixa o áudio do YouTube usando yt-dlp e converte para MP3."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',  # Qualidade do áudio (128, 192, 256, 320)
        }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"Erro ao baixar: {e}")
        return False

def process_track(track, download_path):
    """Processa uma música: busca no YouTube e baixa o áudio."""
    video_url = search_youtube(track)
    if video_url:
        print(f"\n⬇️ Baixando: {track}")
        success = download_audio(video_url, download_path)
        print("✅ Sucesso!" if success else "❌ Falha!")
    else:
        print(f"⚠️ Não encontrado: {track}")
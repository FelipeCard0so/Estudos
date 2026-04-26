from yt_dlp import YoutubeDL


def baixar_video(url, pasta_destino="videos_baixados"):
    opcoes = {
        "outtmpl": f"{pasta_destino}/%(title)s.%(ext)s",
        "format": "bestvideo+bestaudio/best",  # melhor qualidade disponível
        "merge_output_format": "mp4",
        "noplaylist": True
    }

    try:
        with YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        print("\n✔ Download concluído com sucesso!")
    except Exception as e:
        print(f"\n❌ Ocorreu um erro: {e}")


# Exemplo de uso:
url_do_video = input("Cole aqui a URL do vídeo: ")
baixar_video(url_do_video)

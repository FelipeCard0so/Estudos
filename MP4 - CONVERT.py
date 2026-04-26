import os
import subprocess
import math
from datetime import timedelta

# Método 1: Usando FFmpeg diretamente (sem moviepy)
def compressar_video_ffmpeg(caminho_entrada, caminho_saida, bitrate):
    comando = [
        'ffmpeg',
        '-y',  # Sobrescrever arquivo existente
        '-i', caminho_entrada,
        '-c:v', 'libx264',  # Codec de vídeo
        '-b:v', f'{bitrate}k',  # Bitrate de vídeo
        '-preset', 'medium',  # Balanço entre velocidade/compressão
        '-crf', '23',  # Qualidade (0-51, menor é melhor)
        '-c:a', 'aac',  # Codec de áudio
        '-b:a', '128k',  # Bitrate de áudio
        caminho_saida
    ]
    subprocess.run(comando, check=True)

# Método 2: Usando imageio (alternativa ao moviepy)
def compressar_video_imageio(caminho_entrada, caminho_saida, bitrate):
    import imageio.v3 as iio
    from imageio.plugins.ffmpeg import FfmpegFormat

    # Ler metadados do vídeo
    with iio.imopen(caminho_entrada, "r", plugin="pyav") as file:
        duration = file.properties().duration
        fps = file.properties().fps

    # Configurar FFmpeg
    ffmpeg_format = FfmpegFormat("ffmpeg")

    # Escrever vídeo comprimido
    writer = ffmpeg_format.create_writer(
        caminho_saida,
        codec="libx264",
        bitrate=f"{bitrate}k",
        fps=fps,
        input_params=['-y'],
        output_params=['-preset', 'medium', '-crf', '23']
    )

    with writer:
        for frame in iio.imiter(caminho_entrada, plugin="pyav"):
            writer.write(frame)

# Método 3: Usando OpenCV (apenas vídeo, sem áudio)
def compressar_video_opencv(caminho_entrada, caminho_saida, bitrate):
    import cv2

    cap = cv2.VideoCapture(caminho_entrada)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(
        caminho_saida,
        fourcc,
        fps,
        (width, height)
    )

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()

# Funções auxiliares comuns
def calcular_bitrate(tamanho_alvo_mb, duracao_segundos):
    return int((tamanho_alvo_mb * 8192) / duracao_segundos)  # 8 * 1024 = 8192

def listar_arquivos_video(diretorio):
    return [f for f in os.listdir(diretorio) if f.lower().endswith(('.mp4', '.mov', '.avi'))]

def obter_duracao_video(caminho):
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', caminho
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

# Processamento principal
def main():
    diretorio = input("Digite o caminho do diretório onde os vídeos estão: ")
    tamanho_maximo_mb = 5

    for arquivo in listar_arquivos_video(diretorio):
        caminho_completo = os.path.join(diretorio, arquivo)

        if os.path.getsize(caminho_completo) / (1024 * 1024) <= tamanho_maximo_mb:
            print(f"{arquivo} já está abaixo de 199MB. Pulando...")
            continue

        try:
            duracao = obter_duracao_video(caminho_completo)
            bitrate = calcular_bitrate(tamanho_maximo_mb, duracao)
            nome_base = os.path.splitext(arquivo)[0]
            caminho_saida = os.path.join(diretorio, f"{nome_base}_comprimido.mp4")

            print(f"\nComprimindo {arquivo}...")

            # Escolha o método desejado:
            # Método 1 (Recomendado):
            compressar_video_ffmpeg(caminho_completo, caminho_saida, bitrate)

            # Método 2:
            # compressar_video_imageio(caminho_completo, caminho_saida, bitrate)

            # Método 3 (sem áudio):
            # compressar_video_opencv(caminho_completo, caminho_saida, bitrate)

            print(f"Sucesso! Arquivo salvo como: {caminho_saida}")

        except Exception as e:
            print(f"Erro ao processar {arquivo}: {str(e)}")

if __name__ == "__main__":
    main()

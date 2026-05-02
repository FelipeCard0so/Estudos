import os
import subprocess

def compressar_video_ffmpeg(caminho_entrada, caminho_saida, bitrate):
    # Bitrate de vídeo (reservando um pouco para o áudio)
    bitrate_video = int(bitrate - 128) if bitrate > 256 else int(bitrate * 0.8)
    
    comando = [
        'ffmpeg',
        '-y',
        '-i', caminho_entrada,
        '-c:v', 'libx264',
        '-b:v', f'{bitrate_video}k',
        '-maxrate', f'{bitrate}k',
        '-bufsize', f'{bitrate*2}k',
        '-preset', 'medium',
        '-pix_fmt', 'yuv420p', # Resolve problemas de cores/bits do iPhone
        '-c:a', 'aac',
        '-b:a', '128k',
        caminho_saida
    ]
    subprocess.run(comando, check=True)

def calcular_bitrate(tamanho_alvo_mb, duracao_segundos):
    # Cálculo: (MB * 8192 bits) / segundos = kbps
    return int((tamanho_alvo_mb * 8192) / duracao_segundos)

def obter_duracao_video(caminho):
    result = subprocess.run([
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', caminho
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

def main():
    diretorio = input("Digite o caminho da pasta dos vídeos: ").strip()
    tamanho_alvo_mb = 5 # Seu alvo de 5MB

    if not os.path.exists(diretorio):
        print("Pasta não encontrada.")
        return

    pasta_saida = os.path.join(diretorio, "COMPRIMIDOS")
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    extensoes = ('.mp4', '.mov', '.avi', '.mkv')
    arquivos = [f for f in os.listdir(diretorio) if f.lower().endswith(extensoes)]

    for arquivo in arquivos:
        caminho_in = os.path.join(diretorio, arquivo)
        tamanho_atual = os.path.getsize(caminho_in) / (1024 * 1024)

        if tamanho_atual <= tamanho_alvo_mb:
            print(f"SKIPPED: {arquivo} já tem {tamanho_atual:.2f}MB")
            continue

        try:
            duracao = obter_duracao_video(caminho_in)
            bitrate = calcular_bitrate(tamanho_alvo_mb, duracao)
            
            nome_saida = os.path.splitext(arquivo)[0] + ".mp4"
            caminho_out = os.path.join(pasta_saida, nome_saida)

            print(f"\n>>> Comprimindo: {arquivo} ({tamanho_atual:.2f}MB -> Alvo {tamanho_alvo_mb}MB)")
            compressar_video_ffmpeg(caminho_in, caminho_out, bitrate)
            
        except Exception as e:
            print(f"ERRO em {arquivo}: {e}")

if __name__ == "__main__":
    main()

from pydub import AudioSegment
import os

# Solicita o arquivo de entrada
input_file = input("Digite o caminho completo do arquivo MP3: ").strip()

# Verifica se o arquivo existe
if not os.path.isfile(input_file):
    print("Arquivo não encontrado! Verifique o caminho e tente novamente.")
    exit()

# Pergunta o formato desejado
print("\nEscolha o formato de saída:")
print("1 - WAV (alta qualidade)")
print("2 - MP3 (320 kbps / 44.1 kHz)")
opcao = input("Digite 1 ou 2: ").strip()

if opcao not in ["1", "2"]:
    print("Opção inválida!")
    exit()

# Solicita o caminho de saída
output_path = input("\nDigite o caminho de saída (arquivo ou pasta): ").strip()

# Se for apenas pasta
if os.path.isdir(output_path):
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    if opcao == "1":
        output_file = os.path.join(output_path, base_name + "_convertido.wav")
    else:
        output_file = os.path.join(output_path, base_name + "_convertido.mp3")

else:
    # Caminho é arquivo
    if opcao == "1":
        if not output_path.lower().endswith(".wav"):
            output_path += ".wav"
        output_file = output_path
    else:
        if not output_path.lower().endswith(".mp3"):
            output_path += ".mp3"
        output_file = output_path

# Carrega o arquivo original
audio = AudioSegment.from_file(input_file)

# Converte conforme a opção
if opcao == "1":
    # WAV alta qualidade
    audio.export(output_file, format="wav", parameters=["-ac", "2", "-ar", "44100"])
    print("\nArquivo convertido para WAV com sucesso!")
else:
    # MP3 320 kbps / 44.1 kHz
    audio.export(output_file,
                 format="mp3",
                 bitrate="320k",
                 parameters=["-ac", "2", "-ar", "44100"])
    print("\nArquivo convertido para MP3 320 kbps com sucesso!")

print(f"Arquivo salvo em:\n{output_file}")

import os
from PIL import Image

# Caminho para a pasta com as imagens originais
pasta_origem = r'C:\caminho\da\pasta\TRATAMENTO_IMG'  # altere para a pasta das imagens originais

# Caminho para a pasta onde as imagens editadas serão salvas
pasta_destino = r'C:\caminho\da\pasta\TRATAMENTO_IMG\EDITADAS'  # altere p/ a pasta que vai receber as imagens editadas
os.makedirs(pasta_destino, exist_ok=True)


# Função para converter imagens para .jpg e redimensionar
def processar_imagem(caminho_imagem):
    if caminho_imagem.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ithmb', '.webp')):
        imagem = Image.open(caminho_imagem)
        nome_imagem = os.path.splitext(os.path.basename(caminho_imagem))[0] + '.jpg'
        caminho_saida = os.path.join(pasta_destino, nome_imagem)

        # Verifica se a imagem possui transparência (RGBA)
        if 'A' in imagem.getbands():
            imagem = imagem.convert('RGB')  # Converte para o modo de cor RGB se tiver transparência

        imagem.save(caminho_saida, 'JPEG')
        redimensionar_imagem(caminho_saida)


# Função para redimensionar imagens
def redimensionar_imagem(caminho_imagem):
    tamanho_maximo = 5 * 1024 * 1024  # 5MB em bytes
    imagem = Image.open(caminho_imagem)
    largura, altura = imagem.size
    tamanho_atual = os.path.getsize(caminho_imagem)

    while tamanho_atual > tamanho_maximo:
        imagem = imagem.resize((largura // 2, altura // 2), Image.Resampling.LANCZOS)
        imagem.save(caminho_imagem, 'JPEG', quality=85)
        tamanho_atual = os.path.getsize(caminho_imagem)
        largura, altura = imagem.size


# Processamento dos arquivos
for arquivo in os.listdir(pasta_origem):
    caminho_completo = os.path.join(pasta_origem, arquivo)
    # Verifica se é um arquivo de imagem antes de processar
    if os.path.isfile(caminho_completo) and arquivo.lower().endswith(
            ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ithmb', '.webp')):
        processar_imagem(caminho_completo)

print('Processamento concluído!')

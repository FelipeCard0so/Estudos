"""from PIL import Image

# Abra a imagem original
imagem = Image.open("low.jpg")

# Salve como WebP
imagem.save("foto2.webp", format="WEBP")
print("Imagem convertida para WebP!")
"""

import os
from PIL import Image

# Caminho para o diretório atual onde o script está localizado
diretorio = os.getcwd()

# Extensões de imagem suportadas para conversão
extensoes_suportadas = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff",)

# Iterar por todos os arquivos no diretório
for arquivo in os.listdir(diretorio):
    if arquivo.lower().endswith(extensoes_suportadas):
        try:
            # Caminho completo do arquivo
            caminho_completo = os.path.join(diretorio, arquivo)

            # Abrir a imagem
            imagem = Image.open(caminho_completo)

            # Gerar o novo nome com a extensão .webp
            nome_base = os.path.splitext(arquivo)[0]
            novo_nome = f"{nome_base}.webp"
            caminho_webp = os.path.join(diretorio, novo_nome)

            # Salvar a imagem no formato WebP
            imagem.save(caminho_webp, format="WEBP")
            print(f"{arquivo} -> {novo_nome}: Convertido com sucesso!")

            # Fechar o arquivo de imagem para evitar bloqueios no sistema
            imagem.close()

            # Excluir o arquivo original
            os.remove(caminho_completo)
            print(f"{arquivo} excluído com sucesso!")
        except Exception as e:
            print(f"Erro ao converter {arquivo}: {e}")

print("Conversão concluída!")

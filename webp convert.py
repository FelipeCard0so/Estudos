import os
from PIL import Image
from pillow_heif import register_heif_opener

# Registra o suporte para arquivos HEIC no Pillow
register_heif_opener()


def converter_para_webp():
    # Pergunta o diretório ao usuário
    diretorio = input("Digite o caminho da pasta onde estão as imagens (incluindo HEIC): ").strip()

    if not os.path.exists(diretorio):
        print("Erro: O caminho informado não existe.")
        return

    # Cria a pasta 'WEBP'
    pasta_destino = os.path.join(diretorio, "WEBP")
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    # Adicionado .heic na lista de extensões
    extensoes_suportadas = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".heic")

    arquivos = [f for f in os.listdir(diretorio) if f.lower().endswith(extensoes_suportadas)]

    if not arquivos:
        print("Nenhuma imagem compatível encontrada.")
        return

    print(f"Iniciando conversão de {len(arquivos)} imagens...\n")

    for arquivo in arquivos:
        try:
            caminho_origem = os.path.join(diretorio, arquivo)

            # O Pillow agora abre o .heic normalmente graças ao register_heif_opener()
            imagem = Image.open(caminho_origem)

            nome_base = os.path.splitext(arquivo)[0]
            novo_nome = f"{nome_base}.webp"
            caminho_webp = os.path.join(pasta_destino, novo_nome)

            # Salva como WebP
            imagem.save(caminho_webp, format="WEBP", quality=80)

            print(f"✓ {arquivo} -> WEBP/{novo_nome}")
            imagem.close()

        except Exception as e:
            print(f"X Erro ao converter {arquivo}: {e}")

    print("\nProcesso concluído! Tudo pronto na pasta 'WEBP'.")


if __name__ == "__main__":
    converter_para_webp()

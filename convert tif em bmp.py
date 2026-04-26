from PIL import Image
import os

def converter_para_bmp(extensao):
    # Caminho da pasta 'convert' onde estão os arquivos
    pasta_origem = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'convert')
    pasta_destino = os.path.join(pasta_origem, 'bmp')

    # Corrigir extensão se necessário
    if not extensao.startswith('.'):
        extensao = '.' + extensao

    # Criar pasta de destino se não existir
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    total_convertidos = 0

    for nome_arquivo in os.listdir(pasta_origem):
        if nome_arquivo.lower().endswith(extensao):
            caminho_arquivo = os.path.join(pasta_origem, nome_arquivo)
            imagem = Image.open(caminho_arquivo)

            # Converter imagem para RGB para reduzir peso
            if imagem.mode != 'RGB':
                imagem = imagem.convert('RGB')

            # Nome do arquivo de saída
            nome_bmp = os.path.splitext(nome_arquivo)[0] + '.bmp'
            caminho_destino = os.path.join(pasta_destino, nome_bmp)

            # Salvar como BMP (sem canal alfa, menos pesado)
            imagem.save(caminho_destino, format='BMP')

            # Excluir o original
            os.remove(caminho_arquivo)

            print(f"Convertido e excluído: {nome_arquivo} -> {nome_bmp}")
            total_convertidos += 1

    if total_convertidos == 0:
        print(f"Nenhum arquivo com a extensão '{extensao}' encontrado na pasta.")
    else:
        print(f"Conversão concluída! Total de arquivos convertidos: {total_convertidos}")

if __name__ == "__main__":
    print("=== Conversor de Imagens para BMP (leve) ===")
    extensao = input("Digite a extensão dos arquivos que deseja converter (ex: tif, jpg): ").strip().lower()
    converter_para_bmp(extensao)

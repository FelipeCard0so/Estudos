import sys
import os
import pandas as pd

# ========================================================
# FUNÇÃO PARA LOCALIZAR O CAMINHO CORRETO DO .EXE OU SCRIPT
# ========================================================
def get_base_dir():
    """Retorna o caminho da pasta real onde está o .exe ou o script."""
    if getattr(sys, 'frozen', False):  # Executável
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))  # Script normal

BASE_DIR = get_base_dir()

# ========================================================
# LOCALIZAR ARQUIVO EXCEL AUTOMATICAMENTE
# ========================================================
def encontrar_arquivo_excel(nome_parcial):
    for arquivo in os.listdir(BASE_DIR):
        if nome_parcial.lower() in arquivo.lower() and arquivo.endswith(('.xlsx', '.xls')):
            return os.path.join(BASE_DIR, arquivo)
    raise FileNotFoundError(f"Nenhum arquivo Excel encontrado com '{nome_parcial}' na pasta:\n{BASE_DIR}")


# ========================================================
# FUNÇÕES AUXILIARES
# ========================================================
def formatar_site(site):
    """Exemplo: MGXXX → MG-XXX"""
    if isinstance(site, str) and len(site) >= 5:
        return f"{site[:2]}-{site[-3:]}"
    return site


def corrigir_coord(coord):
    """Corrige coordenadas, convertendo vírgulas e removendo valores estranhos"""
    try:
        coord = str(coord).replace(',', '.')
        return float(coord)
    except Exception:
        return ""


# ========================================================
# FUNÇÃO PRINCIPAL
# ========================================================
def main():
    print("📖 Procurando planilha...")

    try:
        input_path = encontrar_arquivo_excel("20250410_Felipe")
    except FileNotFoundError as e:
        print(f"❌ ERRO: {e}")
        input("\nPressione ENTER para sair...")
        return

    output_path = os.path.join(BASE_DIR, "ATIVIDADES_GERADAS.xlsx")

    print(f"✅ Arquivo encontrado: {os.path.basename(input_path)}")
    print("📖 Lendo planilha...")

    df = pd.read_excel(input_path)

    # ====================================================
    # RENOMEAR E SELECIONAR COLUNAS
    # ====================================================
    df_novo = pd.DataFrame()
    df_novo["DEMANDA"] = df["INTEGRADORA"]
    df_novo["INTEGRAÇÃO"] = df["VENDOR"]
    df_novo["SITE"] = df["SITE"].apply(formatar_site)
    df_novo["UF"] = df["REGIONAL"]
    df_novo["TEC"] = df["Tecnologia"]
    df_novo["LAT"] = df["LATITUDE"].apply(corrigir_coord)
    df_novo["LONG"] = df["LONGITUDE"].apply(corrigir_coord)
    df_novo["CIDADE"] = df["CIDADE"]
    df_novo["TEC FINAL"] = df["FREQUENCIA"]
    df_novo["STATUS DA ATIVIDADE"] = "Nova atividade"

    # ====================================================
    # GERAÇÃO DO ARQUIVO FINAL
    # ====================================================
    print("📊 Gerando arquivo de saída...")

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        df_novo.to_excel(writer, index=False, sheet_name="ATIVIDADES")

        workbook = writer.book
        worksheet = writer.sheets["ATIVIDADES"]

        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'vcenter',
            'align': 'center',
            'fg_color': '#009688',
            'font_color': 'white',
            'border': 1
        })

        for col_num, value in enumerate(df_novo.columns.values):
            worksheet.write(0, col_num, value, header_format)

        worksheet.set_column("A:J", 18)
        worksheet.autofilter(0, 0, len(df_novo), len(df_novo.columns) - 1)

    print(f"✅ Planilha gerada com sucesso!\n📁 Local: {output_path}")
    input("\nPressione ENTER para sair...")


# ========================================================
# EXECUÇÃO
# ========================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    finally:
        # Evita erro "lost sys.stdin" em modo .exe sem console
        import sys
        if sys.stdin and sys.stdin.isatty():
            input("\nPressione ENTER para sair...")


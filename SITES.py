"""
VERSÃO AUTOMÁTICA - DT 2.0 (ACABAMENTO FINAL)
"""

import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import unicodedata


# ========================================================
# FUNÇÃO BASE
# ========================================================
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


# ========================================================
# UTILITÁRIAS
# ========================================================
def float_close(a, b, eps=1e-4):
    try:
        return abs(float(a) - float(b)) <= eps
    except Exception:
        return False


def safe_float(value):
    try:
        if pd.isna(value):
            return 0.0
        return float(value)
    except Exception:
        return 0.0


def unique_preserve_order(seq):
    seen = set()
    out = []
    for x in seq:
        if pd.isna(x):
            continue
        if x not in seen:
            seen.add(x)
            out.append(str(x).strip())
    return out


def remove_acentos(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')


# ========================================================
# PROCESSAMENTO
# ========================================================
def process_files(input_path, base_path, out_dir):

    print("📖 Lendo arquivos...")

    df_in = pd.read_excel(input_path, engine='openpyxl')
    df_base = pd.read_excel(base_path, engine='openpyxl')

    os.makedirs(out_dir, exist_ok=True)
    all_texts = []

    mes_ano = datetime.now().strftime("/%m/%Y")

    for idx, row in df_in.iterrows():
        try:
            demanda = str(row["DEMANDA"]).strip().upper()
            integracao = str(row["INTEGRAÇÃO"]).strip().upper()
            site = str(row["SITE"]).strip().upper()
            uf = str(row["UF"]).strip().upper()
            cidade = str(row["CIDADE"]).strip().upper()

            lat = safe_float(row["LAT"])
            lon = safe_float(row["LONG"])

            freq_234_raw = str(row["2G|3G|4G"]).strip()
            freq_5g_raw = str(row["5G"]).strip()

            # ==================================================
            # Buscar PCI / AZIMUTH
            # ==================================================
            matches = []

            for _, brow in df_base.iterrows():
                if (
                    float_close(lat, brow["LATITUDE"])
                    and float_close(lon, brow["LONGITUDE"])
                    and cidade.lower() == str(brow["CIDADE"]).strip().lower()
                ):
                    matches.append(brow)

            pci_list = []
            az_list = []

            if matches:
                for brow in matches:
                    if not pd.isna(brow["PCI"]):
                        pci_list.append(str(int(brow["PCI"])))
                    if not pd.isna(brow["AZIMUTH"]):
                        az_list.append(str(int(brow["AZIMUTH"])))

            pci_str = "/".join(unique_preserve_order(pci_list))
            az_str = "/".join(unique_preserve_order(az_list))

            # ==================================================
            # MONTAGEM TEXTO
            # ==================================================
            lines = [
                f"{uf}-{site}",
                "",
                f"{lat} {lon}",
                "",
                f"({cidade} - {uf})",
                "",
                f"PCI: {pci_str}",
                f"AZIMUTH:  {az_str}",
                "",
                "(Frequências):",
                "",
            ]

            # ==================================================
            # FREQUÊNCIAS (ACABAMENTO LIMPO)
            # ==================================================
            if freq_234_raw and freq_234_raw.lower() != "nan":
                blocos = [b.strip() for b in freq_234_raw.split("|") if b.strip()]
                for bloco in blocos:
                    lines.append(bloco)

            if freq_5g_raw and freq_5g_raw.lower() != "nan":
                # Evita duplicar "5G:"
                if freq_5g_raw.upper().startswith("5G:"):
                    lines.append(freq_5g_raw)
                else:
                    lines.append(f"5G: {freq_5g_raw}")

            lines += [
                "",
                "OBS.>",
                "",
                f"{demanda} - {integracao}",
                "",
                "LOGS armazenados no servidor.",
                f"> Finalizado:  {mes_ano}",
                "",
                "--------------------------- Nome - LOGS --------------------------------------",
                "",
            ]

            # ==================================================
            # LOGS SEGUROS (APENAS 700 e 3500)
            # ==================================================
            safe_integracao = remove_acentos(integracao).replace(" ", "_")
            safe_site = remove_acentos(site).replace(" ", "_")
            safe_city = remove_acentos(cidade).replace(" ", "_")
            safe_uf = remove_acentos(uf)

            nomes_logs = []

            if "700" in freq_234_raw:
                nomes_logs.append(
                    f"_{safe_integracao}_SSV_{safe_site}_4G_700_{safe_city}_{safe_uf}_"
                )

            if "3500" in freq_5g_raw:
                nomes_logs.append(
                    f"_{safe_integracao}_SSV_{safe_site}_5G_3500_{safe_city}_{safe_uf}_"
                )

            lines += nomes_logs
            all_texts.append("\n".join(lines))

        except Exception as e:
            print(f"⚠️ Erro na linha {idx}: {e}")

    separador = "\n" + ("-" * 89 + "\n") * 4 + "\n"
    full_text = separador.join(all_texts)

    out_filename = os.path.join(out_dir, "RELATORIO_SSV_COMPLETO.txt")

    with open(out_filename, "w", encoding="utf-8-sig") as f:
        f.write(full_text)

    print(f"\n✅ Relatório gerado com sucesso!\nArquivo: {out_filename}")


# ========================================================
# EXECUÇÃO
# ========================================================
if __name__ == "__main__":

    input_path = Path(r"C:\Users\User\Desktop\PYTHON\DT - 2.0\ATIVIDADES_GERADAS.xlsx")
    base_path = Path(r"C:\Users\User\Desktop\PYTHON\Base_4G.xlsx")
    out_dir = Path(r"C:\Users\User\Desktop\PYTHON\OUT")

    process_files(input_path, base_path, out_dir)

    try:
        if sys.stdin and sys.stdin.isatty():
            input("\nPressione ENTER para sair...")
    except Exception:
        pass

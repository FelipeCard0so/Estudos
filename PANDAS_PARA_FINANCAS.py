# import pandas as pd
import yfinance as yf

dados_empresa = yf.download("BOVA11.SA", start="2024-02-18", end="2024-03-19")

# selecionando colunas
dados_ajustados = dados_empresa[["Open", "Close", "Volume"]]  # lista de colunas

print(dados_empresa.head())
print(dados_ajustados.head())

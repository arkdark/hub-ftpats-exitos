import requests
from bs4 import BeautifulSoup
import json

URL = "http://www.atscelular.com.br/downloadsversao/"
EXTENSOES_VALIDAS = [".rar", ".zip"]
ARQUIVO_SAIDA = "links.json"

def obter_links():
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as e:
        print("Erro ao acessar a URL:", e)
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    arquivos = []
    for link in links:
        href = link['href']
        if any(href.lower().endswith(ext) for ext in EXTENSOES_VALIDAS):
            nome_arquivo = href.split("/")[-1]
            arquivos.append({
                "nome": nome_arquivo,
                "url": URL + nome_arquivo
            })

    return arquivos

def salvar_json(arquivos):
    with open(ARQUIVO_SAIDA, 'w', encoding='utf-8') as f:
        json.dump(arquivos, f, indent=2, ensure_ascii=False)
    print(f"Arquivo '{ARQUIVO_SAIDA}' gerado com {len(arquivos)} entradas.")

def main():
    print("Buscando links de versões (.rar e .zip)...")
    arquivos = obter_links()
    if arquivos:
        salvar_json(arquivos)
    else:
        print("Nenhum arquivo encontrado.")

if __name__ == "__main__":
    main()

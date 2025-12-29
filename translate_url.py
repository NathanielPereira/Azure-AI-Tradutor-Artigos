"""
translate_url.py
Script para extrair texto de uma URL e traduzi-lo usando Azure OpenAI via langchain_openai.AzureChatOpenAI.

Uso:
  - Configure variáveis de ambiente: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT, AZURE_OPENAI_API_VERSION (opcional)
  - Instale dependências: pip install -r requirements.txt
  - Execute: python translate_url.py -u "https://exemplo.com/artigo" --to pt-br

Observação:
  - Não coloque chaves no repositório; use variáveis de ambiente.
  - Para artigos muito longos, o script pode precisar ser dividido em blocos para evitar limites da API.
"""

import argparse
import logging
import os
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from langchain_openai import AzureChatOpenAI


logger = logging.getLogger(__name__)


def extract_text_from_url(url: str) -> str:
    """Extrai e limpa texto de uma página web."""
    resp = requests.get(url, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"Falha ao recuperar a página. Status code: {resp.status_code}")

    soup = BeautifulSoup(resp.text, 'html.parser')
    for script_or_style in soup(['script', 'style', 'noscript']):
        script_or_style.decompose()

    text = soup.get_text(separator=' ')

    # Limpeza básica: remove múltiplos espaços e quebras desnecessárias
    linhas = (line.strip() for line in text.splitlines())
    parts = (phrase.strip() for line in linhas for phrase in line.split('  '))
    texto_limpo = '\n'.join(part for part in parts if part)

    return texto_limpo


def translate_article(text: str, target_language: str, azure_endpoint: str, azure_key: str, deployment: str, api_version: str = '2023-05-15') -> str:
    """Envia o texto para o Azure OpenAI (via langchain_openai) pedindo a tradução."""
    if not azure_endpoint or not azure_key or not deployment:
        raise RuntimeError('Faltam configurações do Azure OpenAI (endpoint, key ou deployment).')

    client = AzureChatOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_key,
        api_version=api_version,
        deployment_name=deployment,
        max_retries=0
    )

    system_prompt = "Você atua como tradutor de textos. Responda apenas com o conteúdo traduzido em Markdown."
    user_prompt = f"Traduza o texto abaixo para {target_language} e responda em Markdown.\n\n{text}"

    messages = [
        ("system", system_prompt),
        ("user", user_prompt)
    ]

    try:
        response = client.invoke(messages)
        # response.content costuma ter o texto da resposta
        return response.content
    except Exception as e:
        logger.error('Erro durante a chamada ao Azure OpenAI: %s', e)
        raise


def filename_from_url(url: str, lang: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.replace(':', '_')
    path = parsed.path.strip('/').replace('/', '_') or 'index'
    return f"{host}_{path}_{lang}.md"


def main(argv):
    parser = argparse.ArgumentParser(description='Extrai texto de URL e traduz usando Azure OpenAI')
    parser.add_argument('-u', '--url', required=True, help='URL do artigo a ser traduzido')
    parser.add_argument('-t', '--to', default='pt-br', help='Idioma destino (ex: pt-br)')
    parser.add_argument('--endpoint', default=os.environ.get('AZURE_OPENAI_ENDPOINT'), help='Azure OpenAI endpoint (ou use AZURE_OPENAI_ENDPOINT)')
    parser.add_argument('--key', default=os.environ.get('AZURE_OPENAI_KEY'), help='Azure OpenAI key (ou use AZURE_OPENAI_KEY)')
    parser.add_argument('--deployment', default=os.environ.get('AZURE_OPENAI_DEPLOYMENT'), help='Deployment name (ou use AZURE_OPENAI_DEPLOYMENT)')
    parser.add_argument('--api-version', default=os.environ.get('AZURE_OPENAI_API_VERSION', '2023-05-15'))
    parser.add_argument('-o', '--output', help='Arquivo de saída opcional (ex: artigo_pt-br.md)')
    parser.add_argument('--verbose', action='store_true', help='Ativa logs detalhados')

    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format='%(levelname)s: %(message)s')

    try:
        logger.info('Extraindo texto de %s', args.url)
        text = extract_text_from_url(args.url)
        if not text:
            logger.error('Nenhum texto extraído da URL')
            sys.exit(1)

        logger.info('Enviando texto para tradução (Azure OpenAI)')
        translated = translate_article(text, args.to, args.endpoint, args.key, args.deployment, args.api_version)

        out_path = args.output or filename_from_url(args.url, args.to)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(translated)

        logger.info('Tradução salva em: %s', out_path)
        print(out_path)
    except Exception as e:
        logger.error('Erro: %s', e)
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])

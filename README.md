# Azure-AI-Tradutor-Artigos ✅

Projeto que reúne ferramentas para traduzir artigos e documentos usando serviços Azure:

- `tradutor_artigos.py` — traduz arquivos `.docx` (usando Azure Translator Text API).
- `translate_url.py` — extrai texto de uma URL e traduz usando Azure OpenAI (via `langchain_openai`).

Badges
------
- CI: GitHub Actions runs on push to `main` (smoke imports & basic checks).

---

## Rápido começo (Quickstart) 🔧

1. Clone o repositório:

```bash
git clone https://github.com/NathanielPereira/Azure-AI-Tradutor-Artigos.git
cd Azure-AI-Tradutor-Artigos
```

2. Crie um ambiente virtual e instale dependências:

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Configure variáveis de ambiente (NUNCA coloque chaves no código):

PowerShell:

```powershell
$env:AZURE_TRANSLATOR_KEY = "<sua_tradutor_key>"
$env:AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com"
$env:AZURE_TRANSLATOR_REGION = "eastus2"

$env:AZURE_OPENAI_ENDPOINT = "https://<seu-endpoint>.openai.azure.com"
$env:AZURE_OPENAI_KEY = "<sua_openai_key>"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-4.1-mini"
```

4. Exemplos de uso:

- Traduzir `.docx`:

```bash
python tradutor_artigos.py -i "c:\caminho\musica.docx" --to pt-br
```

- Traduzir artigo de uma URL:

```bash
python translate_url.py -u "https://exemplo.com/artigo" --to pt-br
```

---

## Arquivos principais

- `tradutor_artigos.py` — script para traduzir `.docx` com Azure Translator.
- `translate_url.py` — extrai texto web e usa Azure OpenAI para tradução.
- `requirements.txt` — dependências do projeto.
- `README_OPENAI.md` — instruções específicas sobre integração com Azure OpenAI.
- `.github/workflows/ci.yml` — workflow básico de CI (smoke tests).

---

## Observações e boas práticas

- Quebre textos muito longos em blocos antes de enviar à API para evitar limites de prompt e custos elevados.
- Páginas que carregam conteúdo via JavaScript podem precisar de uma ferramenta que execute JS (ex: Playwright) para capturar o conteúdo completo.
- Monitore custos e limites das APIs (Translator / OpenAI).
- Não comite chaves no repositório; utilize GitHub Secrets ou Azure Key Vault em CI.

---

## Licença

Projeto fornecido sem licença específica; adicione um `LICENSE` se desejar tornar isso explícito.

---

Se quiser, eu posso:
- adicionar um badge de CI verdadeiro (quando o workflow rodar com sucesso),
- incluir um teste unitário simples para o CI,
- ou abrir uma PR em vez de push direto para `main` (workflow mais seguro).

Diga o que prefere e eu continuo.
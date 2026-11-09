# PjBL 2 — Assistente FAQ sobre Git e GitHub
Projeto acadêmico de PLN em Python 3.10+, com normalização (v0), TF-IDF + cosseno (v1) e embeddings densos (v2).

## Domínio e fontes
Domínio: uso do Git e GitHub. A base contém pares pergunta/resposta com URL oficial por registro em `dados/base.csv`.
Fontes principais: [Git Book](https://git-scm.com/book/pt-br/v2), [documentação Git](https://git-scm.com/docs) e [documentação GitHub](https://docs.github.com/pt).

## Instalação no Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -c "import nltk; nltk.download('stopwords'); nltk.download('rslp')"
```
O modelo denso é baixado na primeira execução da v2 (internet necessária) e seus vetores são armazenados em cache.

## Uso
```powershell
python chat.py --versao v1
python chat.py --versao v2
python -m src.avaliacao
```
A comparação gera `resultados/comparacao.csv`. A interface de terminal permite conversar com as duas versões.

## Estrutura
`src/normalizacao.py` (v0), `src/chatbot_tfidf.py` (v1), `src/chatbot_denso.py` (v2), `src/avaliacao.py` (métricas), `dados/` (base, validação e teste), `docs/` (decisões e apresentação).

## Método
O conjunto de teste contém 30 paráfrases e 5 perguntas fora do domínio. A validação é separada. Os limiares do código são valores iniciais: o grupo deve selecioná-los usando somente validação e registrar os valores escolhidos antes de avaliar o teste. Não se deve ajustar o limiar olhando o teste.

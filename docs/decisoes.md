# Decisões de projeto

## Domínio e fontes
Git e GitHub. As URLs oficiais das fontes estão registradas em cada linha de `dados/base.csv`.

## v0 — Normalização
A função `normalizar()` permite configurar minúsculas, pontuação, acentos, stopwords e stemming. Manter “não”, “nem” e “sem”, mesmo ao remover stopwords, pois retirar negações pode inverter o sentido. Preservar termos técnicos/siglas como Git, GitHub, API, SSH, URL, README e HEAD durante stemming. A configuração padrão não remove acentos, stopwords nem aplica stemming, evitando perda de informação técnica.

| Pergunta original | Tokens com configuração padrão |
|---|---|
| O que é Git? | o, que, é, git |
| Como criar uma branch? | como, criar, uma, branch |
| Como enviar commits para o GitHub? | como, enviar, commits, para, o, github |
| Qual a diferença entre fetch e pull? | qual, a, diferença, entre, fetch, e, pull |
| Como resolver um conflito de merge? | como, resolver, um, conflito, de, merge |

Expanda a tabela com a saída efetiva do pipeline em configurações alternativas para demonstrar o antes/depois.

## v1 — TF-IDF
As perguntas da base são vetorizadas com TF-IDF e bigramas. O cosseno é calculado manualmente com NumPy e conferido contra scikit-learn. A interface retorna resposta, id, escore e ranking completo. Limiar configurável.

## v2 — Embeddings
Modelo inicial `paraphrase-multilingual-MiniLM-L12-v2`, executado em CPU. Embeddings da base são pré-calculados e salvos em cache. Texto natural original é utilizado, sem remoção de stopwords/stemming.

## Avaliação e análise de erros
O teste contém 30 paráfrases e 5 perguntas fora do domínio. Métricas: Acurácia@1, MRR, rejeição correta e falsa rejeição. A tabela comparativa é gerada automaticamente. Após executar, registrar 3 casos em que v2 supera v1 e 3 casos em que v1 supera v2 (se existirem), com hipóteses; incluir ablação de uma etapa da normalização. Não inventar resultados: preencher com os números gerados pelo script.

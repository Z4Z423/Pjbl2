# Roteiro da apresentação
1. Problema: perguntas sobre Git/GitHub podem ser formuladas de formas diferentes.
2. Objetivo geral: desenvolver e comparar um assistente FAQ com duas representações textuais.
3. Objetivos específicos: normalizar texto, implementar TF-IDF/cosseno, gerar embeddings e medir desempenho.
4. Pesquisa: documentação oficial Git e GitHub; fontes registradas na base.
5. Especificação: Python 3.10+, NLTK, scikit-learn, NumPy e sentence-transformers; CPU.
6. v0: pipeline configurável e preservação de negações.
7. v1: TF-IDF, cosseno manual, ranking e limiar.
8. v2: embeddings pré-treinados e cache.
9. Experimento: 30 paráfrases, 5 perguntas fora do domínio e quatro métricas.
10. Conclusão: inserir os resultados reais de `comparacao.csv` e discutir erros observados.

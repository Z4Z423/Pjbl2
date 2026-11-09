import csv
from pathlib import Path
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .chatbot_tfidf import ChatbotTFIDF
from .chatbot_denso import ChatbotDenso
ROOT=Path(__file__).resolve().parents[1]
def carregar(path):
    with open(path,encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def avaliar(bot,perguntas):
    dentro=[x for x in perguntas if int(x["id_esperado"])!=-1]; fora=[x for x in perguntas if int(x["id_esperado"])==-1]
    acertos=0; rr=[]; falsas=0
    for x in dentro:
        r=bot.responder(x["pergunta"]); ids=[i for i,_ in r.ranking]
        acertos+=bool(ids and ids[0]==int(x["id_esperado"]))
        rr.append(1/(ids.index(int(x["id_esperado"]))+1) if int(x["id_esperado"]) in ids else 0)
        falsas+=(r.id==-1)
    rejeitadas=sum(bot.responder(x["pergunta"]).id==-1 for x in fora)
    return {"acuracia_at_1":acertos/len(dentro),"mrr":float(np.mean(rr)),"rejeicao_correta":rejeitadas/len(fora),"falsa_rejeicao":falsas/len(dentro)}
def calibrar_limiar(bot, validacao, candidatos):
    """Seleciona limiar somente com a validação, sem consultar o teste."""
    melhor_score = float("-inf")
    melhor_limiar = bot.limiar
    for limiar in candidatos:
        bot.limiar = float(limiar)
        m = avaliar(bot, validacao)
        # Dá peso equilibrado à recuperação no domínio e à rejeição fora dele.
        score = (m["acuracia_at_1"] + m["rejeicao_correta"] - m["falsa_rejeicao"]) / 2
        if score > melhor_score:
            melhor_score, melhor_limiar = score, float(limiar)
    bot.limiar = melhor_limiar
    return melhor_limiar

def conferir_cosseno():
    rng=np.random.default_rng(7); a,b=rng.random(20),rng.random(20)
    m=ChatbotTFIDF.cosseno(a,b); s=float(cosine_similarity([a],[b])[0][0])
    assert abs(m-s)<1e-10
    return m,s
def main():
    base=carregar(ROOT/"dados/base.csv")
    validacao=carregar(ROOT/"dados/validacao.csv")
    teste=carregar(ROOT/"dados/teste.csv")
    conferir_cosseno()
    bots={"v1_tfidf":ChatbotTFIDF(base),"v2_embeddings":ChatbotDenso(base)}
    candidatos_v1=[i/100 for i in range(5,61,2)]
    candidatos_v2=[i/100 for i in range(25,81,3)]
    limiares={
        "v1_tfidf":calibrar_limiar(bots["v1_tfidf"],validacao,candidatos_v1),
        "v2_embeddings":calibrar_limiar(bots["v2_embeddings"],validacao,candidatos_v2)
    }
    rows=[{"versao":n,"limiar_validacao":limiares[n],**avaliar(b,teste)} for n,b in bots.items()]
    with open(ROOT/"resultados/comparacao.csv","w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    print("Resultados gravados em resultados/comparacao.csv")
    for r in rows:print(r)
if __name__=="__main__":main()

from dataclasses import dataclass
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from .normalizacao import normalizar
@dataclass
class Resultado:
    resposta:str
    id:int
    escore:float
    ranking:list
class ChatbotTFIDF:
    def __init__(self,base,limiar=0.12,usar_normalizacao=True):
        self.base,self.limiar=base,limiar
        tok=(lambda s:normalizar(s)) if usar_normalizacao else (lambda s:s.split())
        self.vectorizer=TfidfVectorizer(tokenizer=tok,token_pattern=None,lowercase=False,ngram_range=(1,2),sublinear_tf=True)
        self.matriz=self.vectorizer.fit_transform([x["pergunta"] for x in base])
    @staticmethod
    def cosseno(a,b):
        a=np.asarray(a,dtype=float).ravel(); b=np.asarray(b,dtype=float).ravel()
        den=np.linalg.norm(a)*np.linalg.norm(b)
        return float(np.dot(a,b)/den) if den else 0.0
    def responder(self,pergunta):
        if not isinstance(pergunta,str) or not pergunta.strip(): return Resultado("Digite uma pergunta para continuar.",-1,0.0,[])
        q=self.vectorizer.transform([pergunta]).toarray()[0]
        scores=[self.cosseno(q,row.toarray()[0]) for row in self.matriz]
        ranking=sorted([(int(x["id"]),float(s)) for x,s in zip(self.base,scores)],key=lambda z:z[1],reverse=True)
        mid,score=ranking[0]
        if score<self.limiar: return Resultado(f"Não encontrei uma resposta segura (escore={score:.3f}, limiar={self.limiar:.3f}).",-1,score,ranking)
        item=next(x for x in self.base if int(x["id"])==mid)
        return Resultado(item["resposta"],mid,score,ranking)

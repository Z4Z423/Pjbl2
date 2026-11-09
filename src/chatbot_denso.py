from dataclasses import dataclass
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
@dataclass
class Resultado:
    resposta:str
    id:int
    escore:float
    ranking:list
class ChatbotDenso:
    def __init__(self,base,limiar=0.45,modelo_nome="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",cache=True):
        self.base,self.limiar=base,limiar
        self.modelo=SentenceTransformer(modelo_nome,device="cpu")
        self.cache_path=Path(__file__).resolve().parents[1]/"resultados"/"embeddings_base.npy"
        textos=[x["pergunta"] for x in base]
        if cache and self.cache_path.exists():
            try:
                self.embeddings=np.load(self.cache_path)
                if self.embeddings.shape[0]!=len(base): raise ValueError("cache incompatível")
            except Exception: self.embeddings=self._gerar(textos,cache)
        else: self.embeddings=self._gerar(textos,cache)
    def _gerar(self,textos,cache):
        e=self.modelo.encode(textos,convert_to_numpy=True,normalize_embeddings=True)
        if cache: self.cache_path.parent.mkdir(exist_ok=True); np.save(self.cache_path,e)
        return e
    def responder(self,pergunta):
        if not isinstance(pergunta,str) or not pergunta.strip(): return Resultado("Digite uma pergunta para continuar.",-1,0.0,[])
        v=self.modelo.encode([pergunta],convert_to_numpy=True,normalize_embeddings=True)[0]
        scores=self.embeddings@v
        ranking=sorted([(int(x["id"]),float(s)) for x,s in zip(self.base,scores)],key=lambda z:z[1],reverse=True)
        mid,score=ranking[0]
        if score<self.limiar: return Resultado(f"Não encontrei uma resposta segura (escore={score:.3f}, limiar={self.limiar:.3f}).",-1,score,ranking)
        item=next(x for x in self.base if int(x["id"])==mid)
        return Resultado(item["resposta"],mid,score,ranking)

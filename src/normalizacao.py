import re, unicodedata
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
_NEGACOES={"não","nem","sem"}
_SIGLAS={"git","github","api","ssh","https","url","readme","head"}
def _sem_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD",s) if unicodedata.category(c)!="Mn")
def normalizar(texto, *, minusculas=True, remover_pontuacao=True, remover_acentos=False, remover_stopwords=False, stemming=False):
    if not isinstance(texto,str): return []
    s=texto.lower() if minusculas else texto
    if remover_acentos: s=_sem_acentos(s)
    if remover_pontuacao: s=re.sub(r"[^\w\s]"," ",s,flags=re.UNICODE)
    tokens=re.findall(r"\w+",s,flags=re.UNICODE)
    if remover_stopwords:
        try: sw=set(stopwords.words("portuguese"))
        except LookupError: sw=set()
        sw-=_NEGACOES
        tokens=[t for t in tokens if t not in sw or t in _NEGACOES]
    if stemming:
        st=RSLPStemmer()
        tokens=[t if t in _SIGLAS else st.stem(t) for t in tokens]
    return tokens

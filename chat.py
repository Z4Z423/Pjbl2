import argparse
from src.base import carregar_base
from src.chatbot_tfidf import ChatbotTFIDF
from src.chatbot_denso import ChatbotDenso
def main():
    p=argparse.ArgumentParser();p.add_argument("--versao",choices=["v1","v2"],default="v1");a=p.parse_args()
    base=carregar_base();bot=ChatbotTFIDF(base) if a.versao=="v1" else ChatbotDenso(base)
    print(f"FAQ Git/GitHub - {a.versao}. Digite sair para encerrar.")
    while True:
        try:q=input("> ").strip()
        except (EOFError,KeyboardInterrupt):break
        if q.lower() in {"sair","exit","quit"}:break
        r=bot.responder(q);print(f"[{a.versao}] id={r.id} escore={r.escore:.3f}\n{r.resposta}")
        if r.ranking:print("Top 3:",r.ranking[:3])
if __name__=="__main__":main()

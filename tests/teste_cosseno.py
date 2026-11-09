from src.avaliacao import conferir_cosseno
def test_cosseno_manual_confere_com_sklearn():
    a,b=conferir_cosseno()
    assert abs(a-b)<1e-10

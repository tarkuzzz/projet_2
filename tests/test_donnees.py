
from donnees import creation_donnees,nettoyage_donnees



def test_cololmne_df():
    df = creation_donnees()
    assert "raceId" in df.columns
    assert "constructorId" in df.columns
    assert "grid" in df.columns
    assert "positionOrder" in df.columns
    assert "year" in df.columns
    assert "round" in df.columns
    assert "circuitId" in df.columns
    assert "constructorRef" in df.columns
    assert "circuitRef" in df.columns
    assert "country" in df.columns
    assert 'weather' not in df.columns 
    assert len(df.columns) == 10

def test_cololmne_df_nettoyer():
    df_1 = creation_donnees()
    df =  nettoyage_donnees(df_1)
    assert len(df.columns) == 11
    assert 'top10' in df.columns



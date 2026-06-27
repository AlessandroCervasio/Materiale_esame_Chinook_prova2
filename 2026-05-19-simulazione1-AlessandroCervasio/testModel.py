from model.artist import Artist
from model.model import Model

mdl=Model()
mdl.buildGraph(1)
nodi, archi=mdl.getGraphDetails()
print(nodi)
print(archi)

artista, influenza=mdl.getArtistaPiuInfluente()
print(artista)
print(influenza)

archi_p_magg= mdl.getArchiPesoMaggiore()
for a in archi_p_magg:
    print(a)

artista= Artist(1, "AC/DC")

longestPath= mdl.getLongestPath(artista)
for l in longestPath:
    print(l)

camminoPeso= mdl.getCamminoPesoASC(artista)
for c in camminoPeso:
    print(c)
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


        self._chosenGenre=None
        self._chosenArtist= None

    def handleCreaGrafo(self, e):
        if self._chosenGenre is None:
            self._view.create_alert("Selezionare un genere dal menu")
            return
        self._view.txt_result.controls.clear()
        self._model.buildGraph(self._chosenGenre.GenreId)
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        n_nodi, n_archi = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {n_archi}"))

        artista_piu_infl, influenza= self._model.getArtistaPiuInfluente()
        self._view.txt_result.controls.append(ft.Text(f"L'artista più influente è {artista_piu_infl}, con influenza {influenza}"))

        archi_peso_maggiore = self._model.getArchiPesoMaggiore()
        for a in archi_peso_maggiore:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} -> {a[1]}: {a[2]["weight"]}"))

        self._view._btnCreaCammino.disabled=False
        self.fillDDArtist()

        self._view.update_page()

    def handleCammino(self,e):
        if self._chosenArtist is None:
            self._view.create_alert("Selezionare un Artista dal menu")
            return
        longest_path= self._model.getLongestPath(self._chosenArtist)
        cammino_pesoASC= self._model.getCamminoPesoASC(self._chosenArtist)
        self._view.txt_result.controls.append(ft.Text(f"Il cammino più lungo ha {len (longest_path)} nodi:"))
        for l in longest_path:
            self._view.txt_result.controls.append(ft.Text(l))

        self._view.txt_result.controls.append(ft.Text(f"Il cammino semplice di lunghezza max con archi di peso strettamente crescente:"))
        for c in cammino_pesoASC:
            self._view.txt_result.controls.append(ft.Text(c))

        self._view.update_page()


    # metodo fill dropdown
    def fillDDGnere(self):
        genres = self._model.getAllGenres()
        for i in genres:
            self._view._ddGenre.options.append(ft.dropdown.Option(data=i,
                                                                        key=i,
                                                                        on_click=self.chosenGenre
                                                                        ))
    # metodo chosen element dal dropdown
    def chosenGenre(self, e):
        self._chosenGenre = e.control.data
        print(self._chosenGenre)

    def fillDDArtist(self):
        artists = self._model.getAllArtistsGenre(self._chosenGenre.GenreId)
        for i in artists:
            self._view._ddArtist.options.append(ft.dropdown.Option(data=i,
                                                                        key=i,
                                                                        on_click=self.chosenArtist
                                                                        ))

    def chosenGenre(self, e):
        self._chosenGenre = e.control.data
        print(self._chosenGenre)

    def chosenArtist(self, e):
        self._chosenArtist = e.control.data
        print(self._chosenArtist)

    # try:
    #     k_clienti=int(self._view._txt_k_clienti_countries.value)
    #
    # except ValueError:
    #     self._view.create_alert("Inserire un numero intero nell'apposito campo per proseguire!")
    #     return
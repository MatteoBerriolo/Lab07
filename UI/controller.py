import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''
NESSUN_FILTRO = 'Nessun filtro'

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    # POPOLA DROPDOWN
    # Biblioteche: prima la voce "Nessun filtro", poi i nomi letti dal model
    def popola_dropdown(self):
        self._view.dd_biblioteca.options = [ft.dropdown.Option(NESSUN_FILTRO)]
        for nome in self._model.get_biblioteche():
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(nome))

        # Generi: stessa logica
        self._view.dd_genere.options = [ft.dropdown.Option(NESSUN_FILTRO)]
        for genere in self._model.get_generi():
            self._view.dd_genere.options.append(ft.dropdown.Option(genere))

        # Aggiorna la pagina per mostrare le nuove opzioni
        self._view.update()

    # CALLBACKS DROPDOWN
    # Salva la biblioteca scelta; "Nessun filtro" diventa None.
    def handle_biblioteca_selezionata(self, e):
        valore = self._view.dd_biblioteca.value
        self.biblioteca_selezionata = None if valore == NESSUN_FILTRO else valore

    # Salva il genere scelto; "Nessun filtro" diventa None.
    def handle_genere_selezionato(self, e):
        valore = self._view.dd_genere.value
        self.genere_selezionato = None if valore == NESSUN_FILTRO else valore

    # AZIONE: MOSTRA LIBRI
    # Chiede al model i libri filtrati e li mostra nella ListView.
    def handle_mostra_libri(self, e):
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata,
                                               self.genere_selezionato)
        # Svuota la lista dai risultati della ricerca precedente
        self._view.lv_libri.controls.clear()

        # Nessun libro trovato: aggiorna la lista vuota e mostra l'alert
        if not libri:
            self._view.update()
            self._view.show_alert("Nessun libro soddisfa i criteri di filtraggio selezionati.")
            return

        # Una riga di testo per ogni libro. Le chiavi del dizionario (titolo, autore, ...)
        # coincidono con i nomi nella SELECT di libro_DAO.py.
        for libro in libri:
            testo = f"{libro['titolo']} - {libro['autore']} | {libro['genere']} | {libro['biblioteca']}"
            self._view.lv_libri.controls.append(ft.Text(testo))
        self._view.update()


import flet as ft
from UI.alert import AlertManager

'''
    VIEW:
    - Rappresenta l'interfaccia utente
    - Riceve i dati dal MODELLO e li presenta senza modificarli
'''

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Lab07"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # --- Sezione 1: Intestazione ---
        self.txt_titolo = ft.Text(value="Biblioteche di Torino", size=38, weight=ft.FontWeight.BOLD)

        # --- Sezione 2: Filtraggio ---
        # Menu a tendina per la biblioteca. Parte vuoto: le voci le aggiunge il controller
        # (popola_dropdown) dopo aver letto i dati dal database.
        # on_select = funzione chiamata quando scelgo una voce.
        self.dd_biblioteca = ft.Dropdown(
            label="Biblioteca",
            width=300,
            options=[],
            on_select=self.on_select_biblioteca,
        )
        # Menu a tendina per il genere, stessa logica del precedente.
        self.dd_genere = ft.Dropdown(
            label="Genere",
            width=300,
            options=[],
            on_select=self.on_select_genere,
        )
        # Sezione 3: Libri
        # Pulsante che avvia la ricerca. on_click = funzione chiamata al clic.
        self.btn_mostra_libri = ft.Button(
            content="Mostra Libri",
            on_click=self.on_click_mostra_libri,
        )
        # Contenitore che il controller riempie con una riga di testo per ogni libro trovato.
        # L'altezza fissa serve perché la pagina ha già lo scroll.
        self.lv_libri = ft.ListView(
            height=400,
            spacing=5,
            padding=10,
        )

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,

            # Sezione 1
            self.txt_titolo,
            ft.Divider(),

            # Sezione 2: i due dropdown affiancati e centrati
            ft.Row(
                [self.dd_biblioteca, self.dd_genere],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(),

            # Sezione 3: pulsante centrato e, sotto, la lista dei libri
            ft.Row([self.btn_mostra_libri], alignment=ft.MainAxisAlignment.CENTER),
            self.lv_libri,
        )

        self.page.scroll = "adaptive"
        self.page.update()

        # Solo ora che i controlli esistono, chiedo al controller di riempire i dropdown
        # con i dati del database.
        if self.controller is not None:
            self.controller.popola_dropdown()

     # --- Callback verso il controller ---
    # La view non decide nulla: passa l'evento al controller (principio MVC).
    def on_select_biblioteca(self, e):
        self.controller.handle_biblioteca_selezionata(e)

    def on_select_genere(self, e):
        self.controller.handle_genere_selezionato(e)

    def on_click_mostra_libri(self, e):
        self.controller.handle_mostra_libri(e)

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()

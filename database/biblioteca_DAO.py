from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    def get_biblioteche(self):
        """Restituisce la lista dei nomi di tutte le biblioteche."""
        # Prende una connessione dal pool (ne ha solo 3)
        cnx = DBConnect.get_connection()
        # Se la connessione fallisce get_connection() restituisce None: evito di andare in errore
        if cnx is None:
            print("Connessione al database non riuscita.")
            return []

        # dictionary=True: ogni riga è un dizionario, quindi leggo row["nome"]
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT nome FROM biblioteca ORDER BY nome"
        cursor.execute(query)
        # Costruisce la lista dei soli nomi
        risultato = [row["nome"] for row in cursor]
        cursor.close()
        # Restituisce la connessione al pool: va sempre fatto, altrimenti l'app si blocca
        cnx.close()
        return risultato

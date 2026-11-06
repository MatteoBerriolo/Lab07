from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_generi(self):
        """Restituisce la lista dei generi distinti presenti nel database."""
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione al database non riuscita.")
            return []
        cursor = cnx.cursor(dictionary=True)

        # DISTINCT elimina i doppioni; IS NOT NULL evita una voce vuota nel menu
        query = """
            SELECT DISTINCT genere
            FROM libro
            WHERE genere IS NOT NULL
            ORDER BY genere
        """
        cursor.execute(query)
        risultato = [row["genere"] for row in cursor]
        cursor.close()
        cnx.close()  # restituisce la connessione al pool
        return risultato

    def get_libri_filtrati(self, biblioteca, genere):
        """
        Restituisce i libri filtrati per biblioteca e/o genere.
        Un filtro None significa "nessun filtro" (grazie a COALESCE).
        """
        cnx = DBConnect.get_connection()
        if cnx is None:
            print("Connessione al database non riuscita.")
            return []

        cursor = cnx.cursor(dictionary=True)
        # JOIN: il nome della biblioteca sta nella tabella biblioteca, i libri in libro,
        # collegate da libro.id_biblioteca = biblioteca.id.
        # COALESCE(%s, colonna): se il parametro è None usa la colonna stessa, quindi la
        # condizione è sempre vera e quel filtro non agisce. Lo stesso SQL vale con o senza filtro.
        query = """
            SELECT l.titolo, l.autore, l.genere, l.anno_pubblicazione,
                   b.nome AS biblioteca
            FROM libro l
            JOIN biblioteca b ON l.id_biblioteca = b.id
            WHERE b.nome = COALESCE(%s, b.nome)
              AND l.genere = COALESCE(%s, l.genere)
            ORDER BY b.nome, l.titolo
        """
        # I %s vengono riempiti con la tupla: mai concatenare stringhe (SQL injection)
        cursor.execute(query, (biblioteca, genere))
        risultato = cursor.fetchall()
        cursor.close()
        cnx.close()  # restituisce la connessione al pool
        return risultato


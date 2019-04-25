import sqlite3 
from sqlite3 import Error
from privateData import datPath

def create_connection(db_file):
    """ Create a database connection to a SQLite database""" 
    try:
        conn = sqlite3.connect(db_file)
        print('Connection etablished. Version: ' + sqlite3.version)
        return conn
    except Error as e:
        print(e)
    return None

def read_source_data():
    try:
        with open('db/shakespeare.dat', 'r') as file:
            if(file is not None):
                print('DAT file loaded!')
            else:
                print('DAT file not found!')
            return file
    except Error as e:
        print(e)
        print('Error while loading DAT file')
    return None

def create_tables(conn, sqlRequest):
    try:
        c = conn.cursor()
        c.execute(sqlRequest)
        print('table is created')
    except Error as e:
        print(e)
        print('Error while creating tables')

def main():
    conn = create_connection('db/dbExercice.db')

    if conn is not None:
        # Create Personnage table
        fd = open("sql/20192504.001.Install-tPersonnage.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Create Piece table
        fd = open("sql/20192504.002.Install-tPiece.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Create Tirade table
        fd = open("sql/20192504.003.Install-tTirade.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Create Texte table
        fd = open("sql/20192504.004.Install-tTexte.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

    dataSrc = read_source_data()

    










main()






"""
296 |Henry IV       |60 |1.2.180|PRINCE HENRY   |Well, I'll go with thee: provide us all things
297 |Henry IV       |60 |1.2.181|PRINCE HENRY   |necessary and meet me to-morrow night in Eastcheap;
298 |Henry IV       |60 |1.2.182|PRINCE HENRY   |there I'll sup. Farewell.
299 |Henry IV       |61 |1.2.183|POINS          |Farewell, my lord.
300 |Henry IV       |61 |       |POINS          |Exit Poins
...
3203|Henry IV       |8  |5.5.44 |KING HENRY IV  |And since this business so fair is done,
3204|Henry IV       |8  |5.5.45 |KING HENRY IV  |Let us not leave till all our own be won.
3205|Henry IV       |8  |       |KING HENRY IV  |Exeunt
3206|Henry VI Part 1|8  |       |KING HENRY IV  |ACT I

La première colonne est un numéro séquentiel que, faute de meilleur nom, j'appelerai 'id'.
La seconde colonne contient le titre de la pièce.
La troisième colonne est un numéro de tirade (discours d'un personnage). (qui peut être vide)
La quatrième colonne est composée de: (qui peut être vide)
	+ numéro de l'acte
	+ suivi du numéro de la scène dans l'acte
	+ suivi du numéro du vers dans la scène
La cinquième colonne est le nom du personnage. (qui peut être vide)
La sixième colonne (toujours renseignée) est soit:
	+ un vers
	+ un paragraphe en prose
	+ une indication scénique:
        - entrée/sortie de personnage
        - lieu où se passe la scène
        - indication de début d'acte)

1. A part la colonne id dans texte, les identifiants sont générés par le système et auto-incrémentés.
2. La colonne 'id' du fichier de données va dans la colonne id de la table texte.
3. Pour les indications scéniques telle que l'id n°300 ci-dessus, on "oubliera" le nom du personnage (le personnage n'est important que quand il parle).
4. La colonne composite du ficher (numéro d'acte, de scène et de vers) est à éclater pour avoir les numéros d'acte et de scène dans tirades et le numéro de vers dans texte.

"""
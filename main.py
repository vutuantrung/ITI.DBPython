import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Create a database connection to a SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        print('Connection etablished. Version: ' + sqlite3.version)
        return conn
    except Error as e:
        print("Error connecting db: " + e)
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
        print('Error loading DAT file: ' + e)
    return None


def create_tables(conn, sqlRequest):
    try:
        c = conn.cursor()
        c.execute(sqlRequest)
        print('table is created')
    except Error as e:
        print('Error creating tables: ' + e)


def create_personnage(conn, person):
    fd = open("sql/20192504.005.Install-PersonnageInsert.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, person)
    return cur.lastrowid

def search_personnage(conn, person):
    fd = open("sql/20192504.009.Install-PersonnageSearch.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, person)
    rows = cur.fetchall()

    for row in rows:
        print(row)


def create_piece(conn, piece):
    fd = open("sql/20192504.006.Install-PieceInsert.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, piece)
    return cur.lastrowid

def search_piece(conn, piece):
    fd = open("sql/20192504.010.Install-PieceSearch.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, piece)
    rows = cur.fetchall()

    for row in rows:
        print(row)


def create_tirade(conn, tirade):
    fd = open("sql/20192504.007.Install-TiradeInsert.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, tirade)
    return cur.lastrowid


def create_texte(conn, texte):
    fd = open("sql/20192504.008.Install-TexteInsert.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, texte)
    return cur.lastrowid


def main():
    conn = create_connection('db/dbShakespeare.db')

    if conn is not None:
        # Create Personnage table
        fd = open("sql/20192504.001.Install-tPersonnageCreate.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Create Piece table
        fd = open("sql/20192504.002.Install-tPieceCreate.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Create Tirade table
        fd = open("sql/20192504.003.Install-tTiradeCreate.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Create Texte table
        fd = open("sql/20192504.004.Install-tTexteCreate.sql", "r")
        sqlRequest = fd.read()
        create_tables(conn, sqlRequest)

        # Test insert personnage
        person = ('VUTuanTrung',)
        personId = create_personnage(conn, person)

        print(personId)

        search_personnage(conn, person)

    #dtLines = read_source_data()


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
        - indication de début d'acte

1. A part la colonne id dans texte, les identifiants sont générés par le système et auto-incrémentés.
2. La colonne 'id' du fichier de données va dans la colonne id de la table texte.
3. Pour les indications scéniques telle que l'id n°300 ci-dessus, on "oubliera" le nom du personnage (le personnage n'est important que quand il parle).
4. La colonne composite du ficher (numéro d'acte, de scène et de vers) est à éclater pour avoir:
    + les numéros d'acte
    + la scène dans tirades
    + le numéro de vers dans texte.

"""

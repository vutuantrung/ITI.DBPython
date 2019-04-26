import sqlite3
from sqlite3 import Error
import time

def create_connection(db_file):
    """ Create a database connection to a SQLite database"""
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = sqlite3.Row
        print('Connection etablished. Version: ' + sqlite3.version)
        return conn
    except Error as e:
        print("Error connecting db: " + e)
    return None

def read_source_data(conn):
    try:
        with open('db/shakespeare.dat', 'r') as allLines:
            if(allLines is not None):
                for line in allLines:
                    save_line(conn, line)
            else:
                print('DAT file not found!')
    except Error as e:
        print('Error loading DAT file: ' + e)

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
    row = cur.fetchone()

    idPerson = -1
    if(row is not None):
        idPerson = row['id_personnage']

    return idPerson

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
    row = cur.fetchone()

    idPiece = -1
    if(row is not None):
        idPiece = row['id_piece']

    return idPiece

def create_tirade(conn, tirade):
    fd = open("sql/20192504.007.Install-TiradeInsert.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, tirade)
    return cur.lastrowid

def tirade_exist(conn, idTirade):
    sqlRequest = """SELECT * FROM tirades WHERE id_tirade = ?"""
    cur = conn.cursor()
    cur.execute(sqlRequest, (idTirade,))
    row = cur.fetchone()

    if(row is not None):
        return True
    return False

def create_texte(conn, texte):
    fd = open("sql/20192504.008.Install-TexteInsert.sql", "r")
    sqlRequest = fd.read()

    cur = conn.cursor()
    cur.execute(sqlRequest, texte)
    return cur.lastrowid

def create_all_tables(conn):
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

# Get parameters for tirade creation

def create_tirade_object(conn, datas):
    idPiece = get_id_piece(conn, datas[1])

    idPersonnage = None
    if(datas[4] != ""):
        idFound = search_personnage(conn, (datas[4],))
        if(idFound == -1):
            idPersonnage = create_personnage(conn, (datas[4],))
        else:
            idPersonnage = idFound

    numActs = get_num_acts(datas[3])

    numSceneTirade = get_num_scene_tirade(datas[3])

    tiradeObj = (idPiece, idPersonnage, numActs, numSceneTirade, )

    return create_tirade(conn, tiradeObj)

# Get parameters for texte creation

def get_id_piece(conn, pieceTitre):
    piece = (pieceTitre,)
    idFound = search_piece(conn, piece)
    if(idFound != -1):
        return idFound
    else:
        return create_piece(conn, piece)

def get_id_tirade(conn, datas):
    if(datas[2] == ""):
        return None
    
    if(tirade_exist(conn, datas[2]) == False):
        return create_tirade_object(conn, datas)

def get_num_vers(nums):
    if(nums != ""):
        return nums.split('.')[2]
    return None

def get_num_scene_tirade(nums):
    if(nums != ""):
        return nums.split('.')[1]
    return None

def get_num_acts(nums):
    if(nums != ""):
        return nums.split('.')[0]
    return None

def get_nb_rows(conn, nbTypeTable):
    sqlRequest = ""
    if(nbTypeTable == 0):
        print("Nb rows in personnages table:")
        sqlRequest = """SELECT * FROM personnages"""
    elif(nbTypeTable == 1):
        print("Nb rows in pieces table:")
        sqlRequest = """SELECT * FROM pieces"""
    elif(nbTypeTable == 2):
        print("Nb rows in tirades table:")
        sqlRequest = """SELECT * FROM tirades"""
    else:
        print("Nb rows in texte table:")
        sqlRequest = """SELECT * FROM texte"""

    cur = conn.cursor()
    cur.execute(sqlRequest)
    rows = cur.fetchall()
    count = 0
    for row in rows:
        count += 1

    print(count)

def save_line(conn, line):
    datas = line.split('|')

    """
    0 = idtexte
    1 = titre piece
    2 = id tirade
    3 = group of 3 numbers
    4 = nom personnnage
    5 = texte
    """

    idPiece = get_id_piece(conn, datas[1])
    idTirade = get_id_tirade(conn, datas)
    numeroVers = get_num_vers(datas[3])
    texte = datas[5]

    txtObj = (idPiece, idTirade, numeroVers, texte, )
    create_texte(conn, txtObj)

def main():
    start = time.time()
    print('>>>Start process')
    conn = create_connection('db/dbShakespeare.db')
    if conn is not None:
        print('>>>running...')
        create_all_tables(conn)
        read_source_data(conn)
        
    print('>>>End process')
    end = time.time()
    duration = end - start
    
    print('Total duration:')
    print(duration)

    get_nb_rows(conn, 0)
    get_nb_rows(conn, 1)
    get_nb_rows(conn, 2)
    get_nb_rows(conn, 3)

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

create table if not exists personnages (
  id_personnage  integer not null primary key, 
  nom_personnage varchar(20) not null
           constraint longueur_nom_personnage
                check (length(nom_personnage) <= 20),
  constraint nom_personnage_unique unique(nom_personnage))
;
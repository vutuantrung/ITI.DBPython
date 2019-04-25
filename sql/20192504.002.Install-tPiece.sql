create table if not exists pieces (
  id_piece integer not null primary key,
  titre    varchar(30) not null,
  constraint longueur_titre check (length(titre) <= 30),
  constraint titre_unique unique(titre)
);
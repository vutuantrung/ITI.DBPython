create table if not exists texte (
  id          integer not null primary key,
  id_piece    integer not null,
  id_tirade   integer,
  numero_vers integer,
  texte       varchar(1500) not null,
  constraint longueur_texte check (length(texte) <= 1500),
  constraint texte_fk1 foreign key (id_tirade) references tirades (id_tirade),
  constraint texte_fk2 foreign key (id_piece) references pieces (id_piece)
);
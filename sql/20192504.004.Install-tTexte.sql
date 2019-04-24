create table if not exists texte (
  id          int not null primary key,
  id_piece    integer not null,  -- Verification type par FK
  id_tirade   integer,           -- Verification type par FK
  numero_vers integer
           constraint numero_vers_entier
               check(numero_vers is null
                     or (numero_vers+0=numero_vers  -- verification numerique
                         and round(numero_vers)=numero_vers)),
  texte        varchar(1500) not null  -- Il y a des passages en prose
                                       -- qui peuvent etre longs
           constraint longueur_texte
                check (length(texte) <= 1500),
  constraint texte_fk1
    foreign key (id_tirade)
    references tirades (id_tirade),
  constraint texte_fk2
    foreign key (id_piece)
    references pieces (id_piece));
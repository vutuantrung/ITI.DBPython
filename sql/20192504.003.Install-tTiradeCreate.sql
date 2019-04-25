create table if not exists tirades (
    id_tirade     integer not null primary key,
    id_piece      integer not null,
    id_personnage integer not null,
    acte          integer,
    scene         integer,
    constraint tirades_fk1 foreign key ( id_piece ) references pieces ( id_piece ),
    constraint tirades_fk2 foreign key ( id_personnage ) references personnages ( id_personnage )
);
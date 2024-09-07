/* schema.sql */

drop table if exists users;

create table if not exists users (
    id integer primary key,
    username text not null,
    password text not null
);

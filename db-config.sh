#!/usr/bin/env bash

function create_test_database() {
  echo "Creating test database"
  PSQL=psql
  $PSQL \
    -c "CREATE DATABASE testdb4";
}

function create_tables_for_test() {
  echo "Creating tables for test database"
  dbname="testdb4"
  psql $dbname <<SQL
    CREATE TABLE weburlsandtitles (id serial PRIMARY KEY, weburl varchar(65535), title varchar(65535));
    SELECT * FROM weburlsandtitles;
    CREATE TABLE weburls (id serial PRIMARY KEY, weburl varchar(65535));
    SELECT * FROM weburls;
SQL
}

function create_development_database() {
  echo "Creating development database"
  PSQL=psql
  $PSQL \
    -c "CREATE DATABASE testdb5";
}

function create_tables_for_development() {
  echo "Creating tables for development database"
  dbname="testdb5"
  psql $dbname <<SQL
    CREATE TABLE weburlsandtitles (id serial PRIMARY KEY, weburl varchar(65535), title varchar(65535));
    SELECT * FROM weburlsandtitles;
    CREATE TABLE weburls (id serial PRIMARY KEY, weburl varchar(65535));
    SELECT * FROM weburls;
SQL
}

create_test_database
create_tables_for_test
create_development_database
create_tables_for_development

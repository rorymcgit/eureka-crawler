#!/usr/bin/env bash

function create_test_database() {
  echo "Creating test database"
  PSQL=psql
  $PSQL \
    -c "CREATE DATABASE eureka_test";
}

function create_tables_for_test() {
  echo "Creating tables for test database"
  dbname="eureka_test"
  psql $dbname <<SQL
    CREATE TABLE weburlsandcontent (id serial PRIMARY KEY, weburl varchar(65535), title varchar(65535), description varchar(65535), keywords varchar(65535));
    SELECT * FROM weburlsandcontent;
    CREATE TABLE weburls (id serial PRIMARY KEY, weburl varchar(65535));
    SELECT * FROM weburls;
SQL
}

function create_development_database() {
  echo "Creating development database"
  PSQL=psql
  $PSQL \
    -c "CREATE DATABASE eureka_development";
}

function create_tables_for_development() {
  echo "Creating tables for development database"
  dbname="eureka_development"
  psql $dbname <<SQL
    CREATE TABLE weburlsandcontent (id serial PRIMARY KEY, weburl varchar(65535), title varchar(65535), description varchar(65535), keywords varchar(65535));
    SELECT * FROM weburlsandcontent;
    CREATE TABLE weburls (id serial PRIMARY KEY, weburl varchar(65535));
    SELECT * FROM weburls;
SQL
}

create_test_database
create_tables_for_test
create_development_database
create_tables_for_development

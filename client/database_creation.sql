CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA public ;
CREATE OR REPLACE FUNCTION public.create_user() RETURNS VOID
LANGUAGE plpgsql AS
$$
BEGIN
   IF EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE  rolname = 'editor') THEN
      RAISE NOTICE 'Role "my_user" already exists. Skipping.';
   ELSE
      CREATE ROLE editor PASSWORD '1' NOSUPERUSER CREATEDB INHERIT LOGIN;
   END IF;
END
$$;
CREATE OR REPLACE FUNCTION public.create_db(db_name text) RETURNS void
LANGUAGE plpgsql AS
$$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_database WHERE datname = db_name) THEN
        RAISE NOTICE 'database already exists';
    ELSE
        PERFORM dblink_connect('host=localhost user=postgres password = 1'||' dbname=' || current_database());
        PERFORM dblink_exec('CREATE DATABASE ' || quote_ident(db_name) );
    END IF;
END
$$;

ALTER FUNCTION public.create_db(db_name text) OWNER TO postgres;
CREATE OR REPLACE FUNCTION public.drop_db(db_name text) RETURNS void
AS
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = db_name) THEN
        RAISE NOTICE 'database is not exist';
    ELSE
        PERFORM dblink_connect('host=localhost user=postgres password = 1'||' dbname=' || current_database());
        PERFORM dblink_exec('DROP DATABASE ' || quote_ident(db_name) );
    END IF;
END
$$ LANGUAGE plpgsql;
ALTER FUNCTION public.drop_db(db_name text) OWNER TO postgres;

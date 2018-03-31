-- Table: public.categories

-- DROP TABLE public.categories;

CREATE TABLE public.categories
(
  id integer NOT NULL DEFAULT nextval('categories_id_seq'::regclass),
  name character varying(80) NOT NULL,
  description character varying(250),
  parent_id integer,
  CONSTRAINT categories_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.categories
  OWNER TO winejournal;

-- Index: public.ix_categories_parent_id

-- DROP INDEX public.ix_categories_parent_id;

CREATE INDEX ix_categories_parent_id
  ON public.categories
  USING btree
  (parent_id);

-- Table: public.regions

-- DROP TABLE public.regions;

CREATE TABLE public.regions
(
  id integer NOT NULL DEFAULT nextval('regions_id_seq'::regclass),
  name character varying(80) NOT NULL,
  description character varying(250),
  parent_id integer,
  country character varying(20),
  state character varying(20),
  CONSTRAINT regions_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.regions
  OWNER TO winejournal;

-- Table: public.wines

-- DROP TABLE public.wines;

CREATE TABLE public.wines
(
  id integer NOT NULL DEFAULT nextval('wines_id_seq'::regclass),
  name character varying(80) NOT NULL,
  maker character varying(80) NOT NULL,
  price integer,
  description character varying(250),
  region integer,
  category integer,
  vintage character varying(80),
  owner integer,
  CONSTRAINT wines_pkey PRIMARY KEY (id),
  CONSTRAINT wines_category_fkey FOREIGN KEY (category)
      REFERENCES public.categories (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT wines_region_fkey FOREIGN KEY (region)
      REFERENCES public.regions (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.wines
  OWNER TO winejournal;

-- Role: winejournal

-- DROP ROLE winejournal;

CREATE ROLE winejournal LOGIN
  ENCRYPTED PASSWORD 'md587e9435f10f9f1938fdddb61ece04b67'
  NOSUPERUSER INHERIT CREATEDB NOCREATEROLE NOREPLICATION;
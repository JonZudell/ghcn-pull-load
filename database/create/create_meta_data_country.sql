-- Table: "META"."COUNTRIES"

-- DROP TABLE "META"."COUNTRIES";

CREATE TABLE "META"."COUNTRIES"
(
  "CODE" character varying(2) NOT NULL, -- CODE is the FIPS country code of the country where the station is located (from FIPS Publication 10-4 at www.cia.gov/cia/publications/factbook/appendix/appendix-d.html).
  "NAME" character varying(50) NOT NULL -- NAME is the name of the country.
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "META"."COUNTRIES"
  OWNER TO postgres;
COMMENT ON TABLE "META"."COUNTRIES"
  IS '------------------------------
Variable   Columns   Type
------------------------------
CODE          1-2    Character
NAME         4-50    Character
------------------------------

These variables have the following definitions:

CODE       is the FIPS country code of the country where the station is 
           located (from FIPS Publication 10-4 at 
           www.cia.gov/cia/publications/factbook/appendix/appendix-d.html).

NAME       is the name of the country.';
COMMENT ON COLUMN "META"."COUNTRIES"."CODE" IS 'CODE is the FIPS country code of the country where the station is located (from FIPS Publication 10-4 at www.cia.gov/cia/publications/factbook/appendix/appendix-d.html).';
COMMENT ON COLUMN "META"."COUNTRIES"."NAME" IS 'NAME is the name of the country.';


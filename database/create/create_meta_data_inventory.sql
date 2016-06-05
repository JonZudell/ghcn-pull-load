CREATE TABLE "META"."INVENTORY"
(
   "ID" character varying(11) NOT NULL, 
   "LATITUDE" real, 
   "LONGITUDE" real, 
   "ELEMENT" character varying(4), 
   "FIRSTYEAR" integer, 
   "LASTYEAR" integer, 
   CONSTRAINT "INVENTORY_PRIMARY_KEY" PRIMARY KEY ("ID")
) 
WITH (
  OIDS = FALSE
)
;
COMMENT ON COLUMN "META"."INVENTORY"."ID" IS 'ID is the station identification code.  Please see "ghcnd-stations.txt" for a complete list of stations and their metadata.';
COMMENT ON COLUMN "META"."INVENTORY"."LATITUDE" IS 'LATITUDE is the latitude of the station (in decimal degrees).';
COMMENT ON COLUMN "META"."INVENTORY"."LONGITUDE" IS 'LONGITUDE is the longitude of the station (in decimal degrees).';
COMMENT ON COLUMN "META"."INVENTORY"."ELEMENT" IS 'ELEMENT is the element type.  See section III for a definition of elements.';
COMMENT ON TABLE "META"."INVENTORY"
  IS '------------------------------
Variable   Columns   Type
------------------------------
ID            1-11   Character
LATITUDE     13-20   Real
LONGITUDE    22-30   Real
ELEMENT      32-35   Character
FIRSTYEAR    37-40   Integer
LASTYEAR     42-45   Integer
------------------------------

These variables have the following definitions:

ID is the station identification code.  Please see "ghcnd-stations.txt"for a complete list of stations and their metadata.

LATITUDE is the latitude of the station (in decimal degrees).

LONGITUDE is the longitude of the station (in decimal degrees).

ELEMENT is the element type.  See section III for a definition of elements.

FIRSTYEAR is the first year of unflagged data for the given element.

LASTYEAR is the last year of unflagged data for the given element.';

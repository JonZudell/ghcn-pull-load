CREATE TABLE "META"."STATES"
(
   "CODE" character varying(2) NOT NULL, 
   "NAME" character varying(50) NOT NULL, 
   CONSTRAINT "STATES_PRIMARY_KEY" PRIMARY KEY ("CODE", "NAME")
) 
WITH (
  OIDS = FALSE
)
;
ALTER TABLE "META"."STATES"
  OWNER TO postgres;
COMMENT ON COLUMN "META"."STATES"."CODE" IS 'CODE is the POSTAL code of the U.S. state/territory or Canadian  province where the station is located ';
COMMENT ON COLUMN "META"."STATES"."NAME" IS 'NAME is the name of the state, territory or province.';
COMMENT ON TABLE "META"."STATES"
  IS '------------------------------
Variable   Columns   Type
------------------------------
CODE          1-2    Character
NAME         4-50    Character
------------------------------

These variables have the following definitions:

CODE is the POSTAL code of the U.S. state/territory or Canadian province where the station is located 

NAME is the name of the state, territory or province.
';

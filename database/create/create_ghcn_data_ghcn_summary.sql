CREATE TABLE "GHCN_DATA"."GHCN_SUMMARY"
(
  "ID" character varying(11) NOT NULL, -- ID is the GHCN Daily Identification Number
  "TYPE" character varying(20) NOT NULL,
  "VALUE" real NOT NULL, -- VALUE is the value of the observation
  "MONTH" integer NOT NULL, -- MONTH is the Month of observation
  CONSTRAINT "GHCN_SUMMARY_PRIMARY_KEY" PRIMARY KEY("ID","TYPE","MONTH")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "GHCN_DATA"."GHCN_SUMMARY"
  OWNER TO postgres;

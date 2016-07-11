CREATE TABLE "GHCN_DATA"."GHCN_BASE"
(
  "ID" character varying(11) NOT NULL, -- ID is the GHCN Daily Identification Number
  "YEAR" integer NOT NULL, -- YEAR is the Year of observation
  "MONTH" integer NOT NULL, -- MONTH is the Month of observation
  "DAY" integer NOT NULL, -- DAY is the Day of observation
  "HOUR" integer, -- HOUR is the hour of observation if available
  "MINUTE" integer, -- MINUTE is the minute of observation if available
  "ELEMENT" character varying(4) NOT NULL,
  "VALUE" real NOT NULL, -- VALUE is the value of the observation
  "M_FLAG" character, --M_FLAG is the Measurement Flag
  "Q_FLAG" character, --Q_FLAG is the Quality Flag
  "S_FLAG" character, --S_FLAG is the Source Flag
  CONSTRAINT "GHCN_BASE_PRIMARY_KEY" PRIMARY KEY("ID","YEAR","MONTH","DAY")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "GHCN_DATA"."GHCN_BASE"
  OWNER TO postgres;

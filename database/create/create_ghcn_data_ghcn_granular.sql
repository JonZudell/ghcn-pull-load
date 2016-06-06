-- Table: "GHCN_DATA"."GHCN_GRANULAR"

-- DROP TABLE "GHCN_DATA"."GHCN_GRANULAR";

CREATE TABLE "GHCN_DATA"."GHCN_GRANULAR"
(
  "ID" character varying(11) NOT NULL, -- ID is the GHCN Daily Identification Number
  "YEAR" integer NOT NULL, -- YEAR is the Year of observation
  "MONTH" integer NOT NULL, -- MONTH is the Month of observation
  "DAY" integer NOT NULL, -- DAY is the Day of observation
  "HOUR" integer, -- HOUR is the hour of observation if available
  "MINUTE" integer, -- MINUTE is the minute of observation if available
  "ELEMENT" character varying(4) NOT NULL, -- ELEMENT is the type of observation
  "VALUE" real NOT NULL, -- VALUE is the value of the observation
  "M_FLAG" character, --M_FLAG is the Measurement Flag
  "Q_FLAG" character, --Q_FLAG is the Quality Flag
  "S_FLAG" character, --S_FLAG is the Source Flag
  CONSTRAINT "GHCN_GRANULAR_PRIMARY_KEY" PRIMARY KEY ("ID", "YEAR", "MONTH", "DAY", "ELEMENT", "VALUE")
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "GHCN_DATA"."GHCN_GRANULAR"
  OWNER TO postgres;
COMMENT ON TABLE "GHCN_DATA"."GHCN_GRANULAR"
  IS 'ID is the GHCN Station Identifier
YEAR is the year of observation
MONTH is the month of observation
DAY is the day of observation
HOUR is the hour of observation
MINUTE is the minute of observation
ELEMENT is the recorded element
VALUE is the value corelating to the given element';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."ID" IS 'ID is the GHCN Daily Identification Number';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."YEAR" IS 'YEAR is the Year of observation';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."MONTH" IS 'MONTH is the Month of observation';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."DAY" IS 'DAY is the Day of observation';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."HOUR" IS 'HOUR is the hour of observation if available';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."MINUTE" IS 'MINUTE is the minute of observation if available';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."ELEMENT" IS 'ELEMENT is the type of observation';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."VALUE" IS 'VALUE is the value of the observation';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."M_FLAG" IS 'M_FLAG is the Measurement Flag';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."Q_FLAG" IS 'Q_FLAG is the Quality Flag';
COMMENT ON COLUMN "GHCN_DATA"."GHCN_GRANULAR"."S_FLAG" IS 'S_FLAG is the Source Flag';

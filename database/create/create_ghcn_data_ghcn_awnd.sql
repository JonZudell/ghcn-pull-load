CREATE TABLE "GHCN_DATA"."GHCN_AWND" () INHERITS("GHCN_DATA"."GHCN_BASE")
WITH (
  OIDS=FALSE
);
ALTER TABLE "GHCN_DATA"."GHCN_AWND"
  OWNER TO postgres;
ALTER TABLE "GHCN_DATA"."GHCN_AWND"
  ADD CONSTRAINT "GHCN_AWND_PRIMARY_KEY" PRIMARY KEY("ID","YEAR","MONTH","DAY")
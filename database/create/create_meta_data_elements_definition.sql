-- Table: "META"."ELEMENTS_DEFINITION"

-- DROP TABLE "META"."ELEMENTS_DEFINITION";

CREATE TABLE "META"."ELEMENTS_DEFINITION"
(
  "ELEMENT" character varying(4) NOT NULL, -- ELEMENT is the element type.   There are five core elements as well as a number of addition elements.
  "DESCRIPTION" character varying(300), -- DESCRIPTION is the description associated with a given element
  "UNITS" character varying(100) -- UNITS is the units of measurement
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "META"."ELEMENTS_DEFINITION"
  OWNER TO postgres;
COMMENT ON TABLE "META"."ELEMENTS_DEFINITION"
  IS 'ELEMENT is the element type.   There are five core elements as well as a number of addition elements.
  DESCRIPTION is the description associated with a given element
  UNITS is the units of measurement
';
COMMENT ON COLUMN "META"."ELEMENTS_DEFINITION"."ELEMENT" IS 'ELEMENT is the element type.   There are five core elements as well as a number of addition elements.  ';
COMMENT ON COLUMN "META"."ELEMENTS_DEFINITION"."DESCRIPTION" IS 'DESCRIPTION is the description associated with a given element';
COMMENT ON COLUMN "META"."ELEMENTS_DEFINITION"."UNITS" IS 'UNITS is the units of measurement';

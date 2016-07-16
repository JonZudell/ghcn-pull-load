#/usr/bin/python
import psycopg2
import os
import time
import sys

generate_query = '''
INSERT INTO "GHCN_DATA"."GHCN_SUMMARY"(
(SELECT "SUMMED_MONTH_YEAR"."ID" as "ID", 'PRCPAVG' as "TYPE" , AVG("SUMMED_MONTH_YEAR"."VALUE") as "VALUE", "SUMMED_MONTH_YEAR"."MONTH" as "MONTH" FROM (SELECT "ID",SUM("VALUE") AS "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_PRCP"
WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "YEAR", "ID") "SUMMED_MONTH_YEAR"
GROUP BY "SUMMED_MONTH_YEAR"."MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'TMAXAVG' as "TYPE", AVG("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_TMAX" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'TMINAVG' as "TYPE", AVG("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_TMIN" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'SNOWAVG' as "TYPE", AVG("SUMMED_MONTH_YEAR"."VALUE") as "VALUE", "SUMMED_MONTH_YEAR"."MONTH" FROM (SELECT "ID",SUM("VALUE") AS "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_SNOW"
WHERE "ID" = %(id)s  AND "Q_FLAG" IS NULL GROUP BY "MONTH", "YEAR", "ID") "SUMMED_MONTH_YEAR"
GROUP BY "SUMMED_MONTH_YEAR"."MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'SNWDAVG' as "TYPE", AVG("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_SNWD" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'AWDRAVG' as "TYPE", AVG("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_AWDR" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'AWNDAVG' as "TYPE", AVG("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_AWND" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'TAVGAVG' as "TYPE", AVG("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_TAVG" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'TMAXEXTREME' as "TYPE", MAX("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_TMAX" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'TMINEXTREME' as "TYPE", MIN("VALUE") as "VALUE", "MONTH" FROM "GHCN_DATA"."GHCN_TMIN" WHERE "ID" = %(id)s AND "Q_FLAG" IS NULL GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'AVGCDDAYS' as "TYPE", AVG("YEAR_MONTH_COUNT"."COUNT") as "VALUE", "YEAR_MONTH_COUNT"."MONTH" FROM (SELECT COUNT(CASE WHEN "VALUE" > 183 THEN 1 END) AS "COUNT", "MONTH", "ID" FROM "GHCN_DATA"."GHCN_TAVG"
WHERE "ID" = %(id)s GROUP BY "YEAR", "MONTH", "ID") "YEAR_MONTH_COUNT"
GROUP BY "MONTH", "ID" ORDER BY "MONTH")
UNION ALL
(SELECT "ID", 'AVGHDDAYS' as "TYPE", AVG("YEAR_MONTH_COUNT"."COUNT") as "VALUE", "YEAR_MONTH_COUNT"."MONTH" FROM (SELECT COUNT(CASE WHEN "VALUE" < 183 THEN 1 END) AS "COUNT", "MONTH", "ID" FROM "GHCN_DATA"."GHCN_TAVG"
WHERE "ID" = %(id)s GROUP BY "YEAR", "MONTH", "ID") "YEAR_MONTH_COUNT"
GROUP BY "MONTH", "ID" ORDER BY "MONTH"))'''

def get_wmo_stations(cursor):
    cursor.execute('''SELECT "ID" FROM "META"."STATIONS" WHERE "WMO_ID" <> '' ''')
    result = cursor.fetchall()
    result = [ item[0] for item in result ]
    return set(result)

def run(conn):
    cur = conn.cursor()
    stations = get_wmo_stations(cur)

    for station in stations:
        cur.execute(generate_query, { 'id' : station})
        conn.commit()
        

if __name__ == '__main__':
    conn = psycopg2.connect("host='{0}' dbname='{1}' user='{2}' password='{3}'".format(os.environ['INGEST_HOST'],
	                                                                               os.environ['INGEST_DB'],
										       os.environ['INGEST_USER'],
										       os.environ['INGEST_PASS']))
    run(conn)

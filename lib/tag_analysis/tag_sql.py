sql_collection = {

    "create_v_tag_proportion" : """CREATE OR REPLACE VIEW v_tag_proportion AS
                            SELECT
                                to_char(p.creationdate, 'yyyy-mm-dd') AS cdate,
                                p.id,
                                t.tag,
                                1 AS cnt,
                                COUNT(*) OVER (PARTITION BY p.id) AS tot_cnt,
                                (1.0 / COUNT(*) OVER (PARTITION BY p.id))::float AS pct

                            FROM posts p

                            CROSS JOIN LATERAL
                                unnest(string_to_array(trim(both '<>' from p.tags), '><')) AS t(tag)

                            WHERE p.posttypeid = '1'
                            AND p.creationdate BETWEEN %s AND %s
                            AND p.tags LIKE %s
                            AND t.tag <> %s;""",
    "drop_v_tag_proportion" : """DROP VIEW IF EXISTS v_tag_proportion;""",
    "select_v_tag_proportion" : """select * from v_tag_proportion a;"""
}
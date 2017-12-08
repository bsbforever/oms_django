SELECT * FROM (SELECT substr(sql_text,1,40) sql,
rows_processed, executions, rows_processed/executions "Rows/Exec",
hash_value,to_char(sysdate,'YYYY-MM-DD-HH24')
FROM V$SQLAREA
WHERE  executions > 100 ORDER BY executions DESC)
WHERE rownum <= 10

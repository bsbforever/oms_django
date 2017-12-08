SELECT * FROM (SELECT substr(sql_text,1,40) sql,
buffer_gets, executions, buffer_gets/executions "Gets/Exec",
hash_value,to_char(sysdate,'YYYY-MM-DD-HH24')
FROM V$SQLAREA
WHERE buffer_gets > 1000 and executions <>0  ORDER BY buffer_gets DESC)
WHERE rownum <= 10

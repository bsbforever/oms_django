SELECT * FROM (SELECT substr(sql_text,1,40) sql, 
disk_reads, executions, disk_reads/executions "Reads/Exec", 
hash_value,to_char(sysdate,'YYYY-MM-DD-HH24')
FROM V$SQLAREA 
WHERE disk_reads > 1000 and executions <>0  ORDER BY disk_reads DESC) 
WHERE rownum <= 10

select * from (SELECT hash_value, decode(executions,0,1,executions),cpu_time,module,sql_text
FROM V$SQLAREA 
  ORDER BY cpu_time/decode(executions,0,1,executions) DESC)
where rownum<11

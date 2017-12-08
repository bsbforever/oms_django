SELECT   TO_CHAR(sysdate, 'YYYYMMDD HH24:MI:SS') sql_time,
         TO_CHAR(a.logon_time, 'YYYYMMDD HH24:MI:SS') LOGON,
         a.osuser,
         TABLESPACE,
         b.sql_text
  FROM v$session a, v$sql b, v$sort_usage c
 WHERE a.sql_address = b.address
   AND a.saddr = c.session_addr

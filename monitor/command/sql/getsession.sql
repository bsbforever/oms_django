select a.sid,a.serial#,a.username,a.machine,a.program,a.sql_hash_value,a.type,a.LAST_CALL_ET
  from v$session a
 where a.status IN ('ACTIVE', 'KILLED')
 and a.type <> 'BACKGROUND'
  AND a.LAST_CALL_ET>7200
  and a.PROGRAM not like '%CJQ%'
  and a.PROGRAM not like '%QMN%'
  and a.PROGRAM not like '%rman%'
  and a.PROGRAM not like '%P00%'


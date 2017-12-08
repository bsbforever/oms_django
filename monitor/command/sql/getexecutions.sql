select substr (sql_text,0, 40), count (*),max(module)
  from v$sql
 where executions = 1
 group by substr (sql_text,0, 40)
 order by count (*) desc

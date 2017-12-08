select sql_text, hash_value, module , first_load_time, last_load_time
  from v$sql
 where sql_text like '

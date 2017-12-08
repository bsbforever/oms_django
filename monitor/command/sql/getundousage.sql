SELECT round(((SELECT (NVL(SUM(bytes), 0))
           FROM dba_undo_extents
          WHERE tablespace_name = (select value from v$parameter where lower(name) ='undo_tablespace')
            AND status IN ('ACTIVE', 'UNEXPIRED')) * 100) /
       (SELECT SUM(bytes)
          FROM dba_data_files
         WHERE tablespace_name = (select value from v$parameter where lower(name) ='undo_tablespace')),2) PCT_INUSE
  FROM dual

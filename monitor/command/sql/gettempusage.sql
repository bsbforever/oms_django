select round ((s.tot_used_blocks/f.total_blocks)*100, 2) as "percent used"
  from ( select sum (used_blocks) tot_used_blocks
          from v$sort_segment
         where tablespace_name =
               ( select tablespace_name
                  from dba_tablespaces
                 where contents = 'TEMPORARY' and rownum=1)) s,
       ( select sum (blocks) total_blocks
          from dba_temp_files
         where tablespace_name =
               ( select tablespace_name
                  from dba_tablespaces
                 where contents = 'TEMPORARY' and rownum=1)) f

select a.file_name,
       a.bytes / 1024 / 1024 Bytes,
       a.tablespace_name,
       a.autoextensible,
       to_char(b.creation_time, 'yyyy-mm-dd') creation_time
  from dba_data_files a, v$datafile b
 where a.file_id = b.file#
 order by creation_time desc

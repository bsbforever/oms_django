select name ,value from v$sysstat where name in ('sorts (disk)','sorts (memory)') order by name;

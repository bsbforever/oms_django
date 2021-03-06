SELECT OWNER,OBJECT_NAME,OBJECT_TYPE,STATISTIC_NAME,VALUE,SUBOBJECT_NAME   FROM V$segment_Statistics
 WHERE STATISTIC_NAME IN ('logical reads','physical reads','physical writes','buffer busy waits')
 AND OWNER NOT IN ('SYS','SYSTEM',    'OLAPSYS',
                     'XDB',
                     'WKSYS',
                     'ODM_MTR',
                     'SH',
                     'QS_OS',
                     'OUTLN',
                     'PERFSTAT',
                     'QS_WS',
                     'WMSYS',
                     'ODM',
                     'OE',
                     'PM',
                     'QS_ES',
                     'QS_CBADM',
                     'SCOTT',
                     'HR',
                     'APEX_030200',
                     'DBSNMP',
                     'SYSMAN',
                     'IX',
                     'MDSYS',
                     'CTXSYS',
                     'EXFSYS',
                     'ORDSYS',
                     'TSMSYS',
                     'U1',
                     'QUEST')
                     and value >=10000

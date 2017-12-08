select sum (gets),
       sum(getmisses),
       round(( 1 - (sum (getmisses) / (sum(gets) + sum(getmisses)))) * 100,2) HitRate
  from v$rowcache

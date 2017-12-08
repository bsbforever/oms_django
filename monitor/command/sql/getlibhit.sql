select sum (pins) "Eexcutions",
       sum(pinhits) "Hits",
       round((( sum(pinhits) / sum (pins)) * 100),2) "PinHitRatio",
       sum(reloads) "Misses",
      round((( sum(pins) / (sum (pins) + sum(reloads))) * 100),2) "RelodHitRatio"
  from v$librarycache

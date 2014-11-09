rrdtool graph temp.png \
  -s 'now -1 hour' -e 'now' \
  DEF:T_Buero=temperature.rrd:T_Buero:AVERAGE\
  LINE2:T_Buero#00FF00:Buero\
  VDEF:T_Buero_last=T_Buero,LAST \
  "GPRINT:T_Buero_last:%.1lf °C" \
  DEF:T_Aussen=temperature.rrd:T_Aussen:AVERAGE\
  LINE2:T_Aussen#0000FF:Aussen\
  VDEF:T_Aussen_last=T_Aussen,LAST \
  "GPRINT:T_Aussen_last:%.1lf °C" \


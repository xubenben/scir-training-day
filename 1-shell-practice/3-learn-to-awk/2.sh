awk 'BEGIN{num = 0}{num += $2;printf("%s %d\n",$0,num)}' 2.dat

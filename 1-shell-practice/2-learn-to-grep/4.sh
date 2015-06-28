grep -w 'Total:' 4.dat | cut -c 17-26,40-50,64-74 | awk -F"=" '{printf("P=%.2f R=%.2f F=%.2f\n",$1,$2,$3)}'>4.out

awk '{for( i=1 ; i <= NF ; i++){printf("%s",substr($i,1, index($i,"_")-1))};printf("\n")}' 3.dat

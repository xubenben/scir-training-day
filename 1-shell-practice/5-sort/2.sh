sed 's/\t/\n/' query_log.txt | sort | uniq -c | sort -rnk1

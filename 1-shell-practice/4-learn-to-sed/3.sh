for file in `ls`; do mv $file `echo $file | sed 's/\.raw$//'`; done

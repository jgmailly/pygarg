# !/bin/bash

instances_type="ER"


instances_dir="instances/"$instances_type
results_file="results_"$instances_type".csv" # May need to be adapted

rm -f $results_file

nb_instances=`ls $instances_dir/*.apx | wc -l`
cpt=1

for instance in `ls $instances_dir/*.apx`
do
    echo $cpt"/"$nb_instances
    echo -n $instance"," >> $results_file
    for sem in "PR" "CO" "PR" "GR" "ST" "SST" "ID"
    do
	echo $sem
	timeout 600 python3 experiments_PyArg.py $instance $sem > "tmp.txt"
#	timeout 600 python3 experiments.py $instance $sem > "tmp.txt"
	if [ $? -ne 0 ]
	then
	    echo -n "TIMEOUT," >> $results_file
	else
	    runtime=`cat tmp2.txt`
	    echo -n $runtime"," >> $results_file
	fi
    done
    echo " " >> $results_file
    cpt=`expr $cpt + 1`
done

rm -f "tmp.txt"

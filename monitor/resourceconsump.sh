#! /bin/bash
END=$1 ## it will record till 20 secs ## we can pass value by END=$1

while [ $SECONDS -lt $END ]
do 
	echo " docker reource consumption is being capture for CPU $SECONDS seconds"
	docker stats --format="{{.ID}},{{.CPUPerc}},{{.MemUsage}}"  --no-stream | ts '%Y-%m-%d_%H:%M:%S:%s,' > dockercons.tmp1
done
sed 's/%//g' dockercons.tmp1 >> dockercons.tmp2
sed 's/, /,/g' dockercons.tmp2 >> dockercons.tmp3
sed 's: / :,:g' dockercons.tmp3 > dockerres.csv
exit 0;

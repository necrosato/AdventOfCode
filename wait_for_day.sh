 while [[ "$(date | awk '{print $4}' | awk -F':' '{print $1}')" != "21" ]]; do sleep 1; done; ./new_day.sh $1 $2 && vim -p $1/day$2/*

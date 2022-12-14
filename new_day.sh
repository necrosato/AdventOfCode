set -x
dir=$(dirname ${0:a})
ndp=$dir/$1/day$2
mkdir -p $ndp
cp $dir/template/* $ndp
curl --cookie "session=$(cat $dir/cookie)" https://adventofcode.com/$1/day/$2/input | tee $ndp/input

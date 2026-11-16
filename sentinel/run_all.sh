#!/bin/zsh
# runs the sentinel on every coded item (data/key.csv), 4 in parallel -> sentinel/out/sentinel.jsonl
cd "$(dirname $0)/.."
cat sentinel/out/todo.txt | xargs -P 4 -L 1 python3 -I -c '
import sys,json;sys.path.insert(0,"sentinel");import sentinel as S
i,d,t=sys.argv[1:4];r=S.probe(d,t);r["item"]=i;print(json.dumps(r),flush=True)' > sentinel/out/sentinel.jsonl

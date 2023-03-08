REQ_FILE="myrequest.txt"
python sqlmap.py -r $REQ_FILE --eval="import time;current_time=round(time.time())" --dump

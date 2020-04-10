import os
import sqlite3
from encoding import vigEncode
os.environ["FLASK_APP"] = "app.py"


#DONT LOOK AT THIS FUNCTION YOU CHEATER, IT'LL RUIN EVERYTHING
def startup():
    conn = sqlite3.connect('./templates/level1/data.db')
    c = conn.cursor()
    c.execute("DROP TABLE users")
    c.execute("CREATE TABLE users (username text, secret text)")
    for (user, secret) in [("admin",vigEncode("SecretIsInUser554", "SecretIsInUser554")), 
    ("admin",vigEncode("FLAG[LEVEL_1_COMPLETED_YOU_ARE_COOL]", "FLAG[LEVEL_1_COMPLETED_YOU_ARE_COOL]")), 
    ("admin",vigEncode("NotThisOne", "NotThisOne")), ("admin",vigEncode("ThisOneNotHere", "ThisOneNotHere"))]:
        c.execute("INSERT INTO users VALUES ('{}','{}')".format(user, secret))
    conn.commit()

    conn.close()
    conn = sqlite3.connect('./templates/level2/data.db')
    conn.close()
    conn = sqlite3.connect('./templates/level3/data.db')
    conn.close()


startup()

os.system("flask run")
import string
from flask import Flask, request, redirect
import random
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="url_shortener"
)
mycursor = mydb.cursor()
stmt = "SHOW TABLES LIKE 'urls'"
mycursor.execute(stmt)
result = mycursor.fetchone()
if result:
    print("CONNECTED")
else:
    mycursor.execute("CREATE TABLE urls (short_url VARCHAR(255) PRIMARY KEY, long_url VARCHAR(255))")

app = Flask(__name__)


##Generator krótkich kodów
###BAZE DOŁ
##zmianaa
@app.route('/shorten', methods=['POST'])
def shorten_url():
    url = request.form.get('url')
    if not url:
        return "URL is required", 400
    start = "moja_domena"
    digits = random.choices(string.digits, k=3)
    letters = random.choices(string.ascii_letters, k=10)
    end = random.sample(digits + letters, 13)
    url_short = start + end
    sql = "INSERT INTO urls (url_short, url_long) VALUES (%s, %s)"
    urls = (url_short, url)
    mycursor.execute(sql, urls)
    mydb.commit()
    return f"Shortened URL: {url_short}"


@app.route('/<path:url>')
def redirect_url(url):
    mycursor.execute("SELECT url_short, url_long FROM urls")
    url_data = mycursor.fetchall()
    url_dict = {short: long for short, long in url_data}
    if url in url_dict:
        return redirect(url_dict[url])
    else:
        return "URL not found", 404


if __name__ == '__main':
    app.run(port=5001, debug=True)
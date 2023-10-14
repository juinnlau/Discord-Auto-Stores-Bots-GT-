from flask import Flask, request
from pymongo import MongoClient
import json

app = Flask(__name__)

# Membaca nilai dari file config.json
with open('config.json') as config_file:
    config = json.load(config_file)

MONGODB_URL = config['mongodb_url']
DB_NAME = config['dbname']
COLLECTION_NAME = config['collection_name']

client = MongoClient(MONGODB_URL)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

@app.route('/receive', methods=['POST'])
def receive_message():
    message = request.get_data(as_text=True)
    print(f"Pesan dari PowerShell: {message}")

    # Memisahkan nilai balance dan growid dari pesan
    parts = message.split(", ")
    growid = parts[1].split(":")[1].strip().lower()
    balance = int(parts[0].split(":")[1].strip())

    # Mencari data dengan growid yang cocok di dalam koleksi
    existing_data = collection.find_one({'growid': growid})

    if existing_data:
        # Jika data dengan growid cocok ditemukan, tambahkan balance baru ke balance yang ada
        existing_balance = int(existing_data['balance'])
        new_balance = existing_balance + balance
        collection.update_one({'growid': growid}, {'$set': {'balance': new_balance}})
        print(f"Data growid {growid} telah diupdate dengan balance: {new_balance}")
    else:
        print("Growid tidak ditemukan")

    return "Pesan diterima"

if __name__ == '__main__':
    app.run(host='localhost', port=8000)

from flask import Flask, request, jsonify
from pymongo import MongoClient
import redis

client = MongoClient("mongodb://mongo_database", 27017)
redis_client = redis.Redis(host='redis_cache', port=6379)

db = client.user_database
table = db.user_table

post_id = 1
comment_id = 1

app = Flask(__name__)

"""
{
    "username":"",
    "email":"",
    "password":"",
    "dob":"",
    "friends": [{"username":""}],
    "posts": [{"postid":"", "post":"", "likes":}],
    "comments": [{"commentid":"", "postid":"", "comment":""}],
    ],
}
"""

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    table.insert_one({
        'username':data['username'],
        'email':data['email'],
        'password':data['password'],
        'dob':data['dob'],
        'friends': [],
        'posts': [],
        'comments': []
    })
    return "Created New Account"

@app.route('/create_post', methods=['POST'])
def create_post():
    global post_id
    data = request.json
    table.update_one({'username': data['username']}, {'$push': {'posts': {'post_id':post_id, 'post':data['post'], 'likes':0}}})
    post_id += 1
    return "Created Post"

@app.route('/edit_post', methods=['POST'])
def edit_post():
    data = request.json
    table.update_one({'username': data['username'], 'posts.post_id': int(data['post_id'])}, {'$set': {'posts.$.post': data['post']}})
    return 'Updated Post'

@app.route('/delete_post', methods=['POST'])
def delete_post():
    data = request.json
    table.update_one({'username': data['username']}, {'$pull': {'posts': {'post_id': int(data['post_id'])}}})
    return 'Deleted Post'

@app.route('/comment', methods=['POST'])
def comment():
    global comment_id
    data = request.json
    table.update_one({'username': data['username']}, {'$push': {'comments': {'comment_id':comment_id, 'post_id':int(data['post_id']), 'comment':data['comment']}}})


@app.route("/clear", methods=["GET"])
def clear():
    table.delete_many({})
    return "cleared DB"
    

if __name__ =="__main__":
    app.run(host="0.0.0.0", debug=True)


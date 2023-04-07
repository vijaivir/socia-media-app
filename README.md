# socia-media-app

The social media application allows users to create and share posts, it is a demo application that does not include a frontend but can support concurrent users and real-time notifications and messaging. The application is built using Flask (on port 5000) and supports various commands such as add (user), create post, edit post, delete post, comment, and friend request. 

To run the sample script:

'''
docker compose up
'''

In another terminal:

'''
cd backend
python3 input.py test.txt
'''

## 1.0 Components
### 1.1 Database and Cache

The application uses MongoDB to store information about the system and a implements a Redis cache to store frequently accessed data and improved performance. Both the MongoDB and Redis cache are exposed on the default ports 27017 and 6379 respectively.   The database uses the following schema to store user information:

'''
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
'''

###1.2 NGINX Load Balancer

An NGINX load balancer has been configured to handle user loads by distributing incoming requests to multiple servers and improve availability. It acts as a reverse proxy that listens on port 80 and forwards incoming requests to the backend server:

'''
events {
    worker_connections 1000;
}
http {
    server {
        listen 80;
        location / {
            proxy_pass http://backend:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
'''


###1.3 RabbitMQ
The application supports real-time notifications using RabbitMQ for friend requests between users. It uses a fanout exchange and uses the main port 5672. 

'''
@app.route("/friend_request", methods=["POST"])
def friend_request():
    data = request.json
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.exchange_declare(exchange='friend_requests', exchange_type='fanout')
    data = {
        'from_user': data['from_user'],
        'to_user': data['to_user']
    }
    channel.basic_publish(exchange='friend_requests', routing_key='', body=json.dumps(data))
    connection.close()
    return "request received"
'''


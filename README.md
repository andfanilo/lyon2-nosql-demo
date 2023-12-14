# NoSQL Docker demo

Here is a Docker compose file which starts redis, mongo, cassandra and Orientdb containers for demonstration purposes.

## Cluster

If you want to start all at once !

Start : `docker-compose up`

Dismount : `docker-compose down`

## Python

Connect to Python : `docker exec -it mypython bash`

Run: `pip install redis pymongo cassandra-driver pyorient`

## Redis

### Command line

Connect to redis : `docker exec -it myredis redis-cli`

```sh
ping
ping "hello world"

set hello world
get hello

keys *

incr next.recordings.id

sadd recordings:1:artist "Rolling Stones"
sadd recordings:1:title "Beggars banquet"
sadd recordings:1:price 9.99

keys *

smembers recordings:1:artist
srem recordings:1:artist "Rolling Stones"
```

### IPython

```python
import redis

r = redis.Redis(host='myredis', port=6379)
r.set('foo', 'bar')
r.get('foo')
```

## Mongo

### Command line

Connect to mongo : `docker exec -it mymongo mongo`

```sh
use rainforest
album ={
  id:1,
  artist: "Rolling Stones",
  price: 9.99
}
db.recordings.insert(album)
db.recordings.find()
db.recordings.remove({id:1})
db.recordings.find()
```

### IPython

```python
import pymongo
from pymongo import MongoClient

client = MongoClient('mymongo', 27017)
test_db = client.test_database
posts = test_db.posts

post = {
    "author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
}
post_id = posts.insert_one(post).inserted_id

posts.find_one()

posts.insert_one({
    "author": "Fanny",
    "text": "My first blog post!",
    "tags": ["java"],
})
posts.find_one({"author": "Fanny"})
```

## Cassandra

### Command line

Connect to Cassandra : `docker exec -it mycassandra cqlsh`

```sh
CREATE KEYSPACE rainforest WITH replication = {'class':'SimpleStrategy', 'replication_factor':'1'};
USE rainforest;
CREATE COLUMNFAMILY recordings(
title varchar PRIMARY KEY,
artist varchar, 
price double);
INSERT INTO recordings (title, artist, price) values ('Tattoo You', 'Stones', 9.99);
Select * from recordings;
CREATE INDEX ON recordings(artist);
SELECT * from recordings where artist='Stones';
```

### IPython

```python
from cassandra.cluster import Cluster

cluster = Cluster(['mycassandra'], port=9042)
session = cluster.connect()

session.execute("CREATE KEYSPACE rainforest WITH replication = {'class':'SimpleStrategy', 'replication_factor':'1'}")
session.set_keyspace('rainforest')
session.execute("CREATE COLUMNFAMILY recordings(title varchar PRIMARY KEY, artist varchar, price double)")
session.execute("INSERT INTO recordings (title, artist, price) values ('Tattoo You', 'Stones', 9.99);")
session.execute("INSERT INTO recordings (title, artist, price) values ('Music', 'Madonna', 19.99);")

rows = session.execute('SELECT artist, title FROM recordings')
for user_row in rows:
    print(user_row.artist, user_row.title)
```

## Neo4j

### Command line

Connect to OrientDB : `docker exec -it myorientdb bash`

### IPython

```python
import pyorient

ROOT_PASSWORD = "root"
client = pyorient.OrientDB("myorientdb", 2424)
session_id = client.connect("root", ROOT_PASSWORD)

client.db_create("gods", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)
client.db_open( "gods", "root", ROOT_PASSWORD) 

client.command("create vertex content {name: 'Zeus', symbol: 'thunder'}")
client.command("create vertex content {name:'Héra', symbol:'tiara'}")
client.command("create vertex content {name:'Poséidon', symbol:'trident'}") 
client.command("create vertex content {name:'Athena', symbol:'helmet'}")
client.command("create vertex content {name:'Arès', symbol:'weapons'} ") 

client.command("create edge from (SELECT FROM V WHERE name = 'Zeus') to (SELECT FROM V WHERE name = 'Poséidon') content {kind: 'sibling'}")

for i, o, c in [
    ('Zeus','Héra','sibling'),
    ('Zeus','Arès','father'),
    ('Zeus','Athena','father'),
    ('Héra','Arès','mother'),
    ('Héra','Zeus','sibling'),
    ('Poséidon','Zeus','sibling')
]:
    command=f"create edge from (select from V where name = '{i}') to (select from V where name = '{o}') content {{kind: '{c}'}}"
    print(command)
    client.command(command)
```

Browser is available via http://localhost:2480

```
select expand(out()) from V where name = 'Zeus'
select expand(in) from E where kind = 'father'
select from V where out_ in (select from E where kind = 'mother')
```
# NoSQL Docker demo

Here is a Docker compose file which starts redis, mongo, cassandra and neo4j containers for demonstration purposes.

## Python

```sh
conda create -n nosql python=3.8
conda activate nosql
pip install redis pymongo cassandra-driver neo4j jupyter
```

## Cluster

If you want to start all at once !

Start : `docker-compose up`

Dismount : `docker-compose down`

## Redis

Run Redis server : `docker-compose run --rm --name myredis redis`

### Command line

Connect to redis : `docker exec -it myredis bash; redis-cli`

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

r = redis.Redis(host='localhost', port=6379)
r.set('foo', 'bar')
r.get('foo')
```

## Mongo

Run Mongo server : `docker-compose run --rm --name mymongo mongo`

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

client = MongoClient('localhost', 27017)
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

Run Cassandra server : `docker-compose run --rm --name mycassandra cassandra`

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

cluster = Cluster()
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

Run Neo4j server : `docker-compose run --rm --service-ports --name myneo4j neo4j`

### Command line

Connect to Neo4j : `docker exec -it myneo4j cypher-shell`

Neo4j Browser is available via HTTP at http://localhost:7474 and HTTPS at https://localhost:7473.

```sh
CREATE (a { artist: 'Rolling Stones' });
CREATE (t { title: 'Beggars Banquet' });

MATCH (a),(t)
WHERE a.artist = 'Rolling Stones' AND t.title = 'Beggars Banquet'
CREATE (a)-[r:ARTIST]->(t)
RETURN r;

MATCH (rolling_stones)-[:ARTIST]-(recordings)
WHERE rolling_stones.artist = 'Rolling Stones' 
RETURN recordings.title;
```

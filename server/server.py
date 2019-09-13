#!/usr/bin/env python3
import sys
import json
from flask import Flask
from flask import request
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient



app = Flask(__name__)

# semi-safe casting str to int
def sint(v) :
    try :
        return(int(v))
    except (ValueError, TypeError) :
        return(float("NaN"))



# class fetching docs from mongodb not more than once in <expire>
class News : 

    def __init__(
        self,
        host = "db",
        port = 27017,
        db = "hnews",
        coll = "hnews",
        expire = timedelta(seconds = 60)
    ) :
        self.client = MongoClient(host, port)
        self.db = self.client[db][coll]
        self.last = None
        self.expire = expire
        self.data = None

    def get(self) :
        now = datetime.now()
        if not self.last or now - self.last > self.expire :
            self.last = now
            self.data = list(self.db.find({}, {"_id" : 0})) # hiding _id
        return(self.data)



# as stand-alone fn for testing purposes
def process_posts_query(posts, order, sort, offset, limit) :
    
    # [x<N>] -> [{id: <N> | x<N>}]
    def map_id(posts, start = 1) :
        for p in posts :
            p["id"] = start
            start += 1

    fields = posts[0].keys() if posts else [] # field name list 
    sortK = {"asc" : False, "desc" : True} 

    limit = limit if limit >= 0 else 5 # ¯\_(ツ)_/¯ # len(posts)
    if limit == 0 :
        return([])

    sort = sort if sort in sortK.keys() else "asc"

    sortF = lambda : None # NoOp if <order> ∉ <fields>, sort by <order> otherwise
    if order in fields :
        sortF = lambda : posts.sort(
            key = lambda i : i[order],
            reverse = sortK[sort]
        )

    offset = offset if offset >= 0 else 0
    if offset >= len(posts) :
        return([])

    sortF()
    map_id(posts)

    return(posts[offset : offset + limit])



# .../posts?[order=<field>[&sort=asc|desc]][offset=n:n>=0][limit=n:n>=0]
@app.route('/posts')
def serve_posts() :

    posts = process_posts_query(
        posts = news.get(),
        order = request.args.get("order"),
        sort = request.args.get("sort"),
        offset = sint(request.args.get("offset")),
        limit = sint(request.args.get("limit"))
    )

    return(
        json.dumps(
            posts
        )
    )



if __name__ == '__main__' :
    news = News()
    app.run(host='0.0.0.0')

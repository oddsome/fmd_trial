#!/usr/bin/env python3
import xmltodict
import urllib.request



# url -> [{news}]
def get_news() :
    
    def req(url) :
        try:
            return(urllib.request.urlopen(url).read().decode('utf-8'))
        except Exception as _:
            exit("Network error")
    
    hn = "https://news.ycombinator.com/rss"
    news = xmltodict.parse(req(hn))["rss"]["channel"]["item"]
    return(news)



if __name__ == "__main__":
    import sys
    import time
    import hashlib
    import datetime
    from pymongo import MongoClient



    # xN -> {_id: <stamp>, created: <now> | xN \ description \ comments \ pubDate}
    def prep(n) :

        def gen_id(s) : 
            _id = hashlib.md5(s.encode('utf-8')).hexdigest()
            return _id

        n.pop("description", None)
        n.pop("comments", None)
        date = n.pop("pubDate", None)
        n["_id"] = gen_id(n["title"] + date)
        n["created"] = datetime.datetime.now().isoformat() # ISO 8601
        return(n)

    # write only if there were no such _id: <stamp>
    def update_db(db, news) : 
        for n in news :
            db.update_one(
                {"_id" : n["_id"]},
                {"$setOnInsert" : n},
                upsert = True
            )

    delay = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    client = MongoClient("db", 27017)
    db = client["hnews"]["hnews"]

    while True:
        news = get_news()
        db_items = list(
            map(
                prep,
                news
            )
        )
        update_db(db, db_items)
        time.sleep(delay)

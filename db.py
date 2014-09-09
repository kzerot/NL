import psycopg2
from psycopg2.extras import DictCursor
from collections import OrderedDict
import json as pyjson

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=north host=91.185.48.86 user=north password=q1w2e3",
            cursor_factory=DictCursor)

    def uniGet(self, id, table):
        cur = self.conn.cursor()
        query = '''select get_object('%s', %d) as data,
                get_object('%s', parent_id) as init_data from %s where id = %d''' \
                % (table, id, table, table, id)
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        res['data'] = OrderedDict(sorted(res['data'].items(),
                                  key=lambda t: t[0]))
        return {"data": res['data'], "init_data": res["init_data"]}

    def uniGetAllWeb(self, table):
        cur = self.conn.cursor()
        query = "select id, parent_id, get_object('%s', id) as data from %s" \
                % (table, table)
        cur.execute(query)
        res = cur.fetchall()
        cur.close()
        l = []
        for item in res:
            result_item = {}
            result_item["id"] = item['id']
            parent = '#'
            if item['parent_id'] and item["parent_id"] != "":
                parent = item['parent_id']
            result_item["parent"] = parent
            result_item["text"] = item["data"]["name"]
            result_item['data'] = item["data"]
            l.append(result_item)
        return l

    def getItem(self, id):
        return self.uniGet(id, 'items')

    def getItemsAll(self):
        return self.uniGetAll('items')

    def getItemsAllWeb(self):
        return self.uniGetAllWeb('items')

    def addItem(self, itemId, name, table="items"):
        cur = self.conn.cursor()
        json = {'name': name}
        if not itemId or itemId == '#':
            itemId = 'null'
        query = '''insert into %s (data, parent_id) values ('%s', %s)''' % (table, pyjson.dumps(json), itemId)
        print(query)
        cur.execute(query)
        query = '''select max(id) from %s''' % table
        cur.execute(query)
        res = cur.fetchone()
        query = "select id, parent_id, get_object('%s', id) as data from %s where id = %d" \
                % (table, table, res[0])
        cur.execute(query)
        item = cur.fetchone()
        result_item = {}
        result_item["id"] = item['id']
        parent = '#'
        if item['parent_id'] and item["parent_id"] != "":
            parent = item['parent_id']
        result_item["parent"] = parent
        result_item["text"] = item["data"]["name"]
        self.conn.commit()
        cur.close()
        return result_item

    def deleteProp(self, itemId, node, table="items"):
        cur = self.conn.cursor()
        query = '''select data from %s where id = %d''' \
                % (table, itemId)
        cur.execute(query)
        res = cur.fetchone()
        #cur.close()
        json = res["data"]
        if node in json:
            print("delete node ", node)
            del json[node]

        query = '''update %s set data='%s' where id = %s''' % (table, pyjson.dumps(json), itemId)
        cur = self.conn.cursor()
        #print(cur.mogrify(query))
        cur.execute(query, (table, pyjson.dumps(json), itemId))
        cur.close()
        self.conn.commit()
        return True

    def deleteItem(self, itemId, table="items"):
        cur = self.conn.cursor()
        query = '''delete from %s where id = %d''' % (table, itemId)
        if itemId:
            cur.execute(query)
            self.conn.commit()
            return {"result": True}
        return {"result": False}

    def updateItem(self, itemId, json, table="items"):
        cur = self.conn.cursor()
        query = '''update %s set data='%s' where id = %s''' % (table, pyjson.dumps(json), itemId)
        cur.execute(query)
        cur.close()
        self.conn.commit()
        return True

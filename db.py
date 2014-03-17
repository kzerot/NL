import psycopg2
from psycopg2.extras import DictCursor
from collections import OrderedDict

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=north host=evillord.ru user=north password=q1w2e3",
            cursor_factory=DictCursor)

    def uniGet(self, id, table):
        cur = self.conn.cursor()
        query = '''select get_object('%s', %d) as data,
                data as init_data from %s where id = %d''' \
                % (table, id, table, id)
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

    def deleteItem(self, itemId, node, table="items"):
        cur = self.conn.cursor()
        query = '''select data from %s where id = %d''' \
                % (table, itemId)
        cur.execute(query)
        res = cur.fetchone()
        #cur.close()
        json = res["data"]
        if node in json:
            del json[node]

        query = '''update %s set data=%s where id = %s'''
        cur = self.conn.cursor()
        cur.execute(query, (table, json, itemId))
        cur.close()
        return True

    def updateItem(self, itemId, json, table="items"):
        cur = self.conn.cursor()
        query = '''update %s set data=%s where id = %s'''
        cur = self.conn.cursor()
        cur.execute(query, (table, json, itemId))
        cur.close()
        return True

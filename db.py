import psycopg2
from psycopg2.extras import DictCursor


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            "dbname=north host=evillord.ru user=north password=q1w2e3",
            cursor_factory=DictCursor)

    def uniGet(self, id, table):
        cur = self.conn.cursor()
        query = "select get_object('%s', %d)" % (table, id)
        cur.execute(query)
        res = cur.fetchone()
        cur.close()
        return res

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
            if item['parent_id'] and item["parent_id"]!="":
                parent = item['parent_id']
            result_item["parent"] = parent
            result_item["text"] = item["data"]["name"]
            result_item['data'] = item["data"]
            l.append(result_item)
        return l

    def getItem(self, id):
        return self.uniGet('items')

    def getItemsAll(self):
        return self.uniGetAll('items')

    def getItemsAllWeb(self):
        return self.uniGetAllWeb('items')

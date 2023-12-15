import mariadb
import gi

gi.require_version("GLib", "2.0")

from gi.repository import GLib

from date_utils import DateUtils

class DataAccess():
    def __init__(self):
        super().__init__()

    def getConnection(self):
        try:
            conn = mariadb.connect(user="username", password="password", host="localhost", port=3306, database="produtos")
            return conn
        except mariadb.Error as e:
            print(f"Falha ao conectar ao MariaDB: {e}")
        return None

    def getAll(self):
        sql = "SELECT idproduto, produto, FORMAT(quantidade, 2), un, FORMAT(punitario, 2), CAST(quantidade * punitario AS DECIMAL(10, 2)) AS total FROM produto ORDER BY produto"

        conn = self.getConnection()
        cur = conn.cursor()

        result = []

        try:
            cur.execute(sql)

            for line in cur:
                result.append(line)
        except mariadb.Error as e:
            print(f"Erro ao executar a SQL: {e}")
        
        conn.close()
        return result

    def insertNovoItem(self, item):
        sql = "INSERT INTO produto (produto, quantidade, un, punitario) VALUES ('%s', %s, '%s', %s)" % (item[0][0],item[0][1], item[0][2], item[0][3])
        
        conn = self.getConnection()
        cur = conn.cursor()

        try:
            cur.execute(sql)
        except mariadb.Error as e:
            print(f"Error: {e}")
        
        conn.commit()
        last_row_id = cur.lastrowid
        conn.close()

        return last_row_id
    
    def getMaxNfNumber(self):
        sql = "SELECT MAX(nf) FROM vendas"

        conn = self.getConnection()
        cur = conn.cursor()

        result = []

        try:
            cur.execute(sql)

            for line in cur:
                result.append(line)
        except mariadb.Error as e:
            print(f"Erro ao executar a SQL: {e}")
        
        conn.close()
        return result
    
    def finalizar_venda(self, itens, nf):
        date_utils = DateUtils()

        date = date_utils.currentDate()
        
        sql = ""
        
        for i in range(len(itens)):
            sql = "INSERT INTO vendas(nf, idproduto, produto, quantidade, punitario, data) VALUES(%s, %s, '%s', %s, %s, '%s')" % (nf, itens[i].idproduto, 
                itens[i].produto, itens[i].quantidade, itens[i].punitario, date)
            
            result = []
            
            conn = self.getConnection()
            cur = conn.cursor()

            try:
                cur.execute(sql)
            except mariadb.Error as e:
                print(f"Error: {e}")
            
            conn.commit()
            
            conn.close()
            
        self.debtProdutos(itens)

        return True

    def debtProdutos(self, itens):
        sql = ""

        for i in range(len(itens)):
            sql = "UPDATE produto SET quantidade = quantidade - %s WHERE idproduto = %s" % (itens[i].quantidade, itens[i].idproduto)

            conn = self.getConnection()
            cur = conn.cursor()
            
            try:
                cur.execute(sql)
            except mariadb.Error as e:
                print(f"Error: {e}")
            
            conn.commit()

            conn.close()

    def getVendaByNf(self, nf):
        sql = "SELECT idvenda, idproduto, produto, quantidade, punitario, CAST(quantidade * punitario as decimal(10,2)), \
            DATE_FORMAT(data, '%%d/%%m/%%Y %%H:%%m:%%S'), nf FROM vendas WHERE nf = %s" % (nf)
        
        conn = self.getConnection()
        cur = conn.cursor()

        result = []

        try:
            cur.execute(sql)

            for line in cur:
                result.append(line)
        except mariadb.Error as e:
            print(f"Erro ao executar a SQL: {e}")
        
        conn.close()
        return result
        
    def getTotalGeral(self, nf):
        sql = "SELECT CAST(SUM(quantidade * punitario) AS DECIMAL(10, 2)) FROM vendas WHERE nf = %s" % (nf)

        conn = self.getConnection()
        cur = conn.cursor()

        result = []

        try:
            cur.execute(sql)

            for line in cur:
                result.append(line)
        except mariadb.Error as e:
            print(f"Erro ao executar a SQL: {e}")
        
        conn.close()
        return result

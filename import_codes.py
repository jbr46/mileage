import csv
import pymysql.cursors

def main():
    connection = pymysql.connect(host='34.171.138.243',
                             user='jbr46',
                             password='mileage',
                             database='mileage',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

    with connection:
        with connection.cursor() as cursor:
            with open("codes.RGS") as f:
                reader = csv.reader(f, delimiter=' ')
                for count, row in enumerate(reader):
                    if count <= 6:
                        pass
                    elif row[0] == '/':
                        station = row[1]
                        word = 2
                        while word < len(row) and row[word] != '(a':
                            station += (' ' + row[word]) 
                            word += 1
                        stack = []
                        stack.append(station)
                        sql = "INSERT INTO `stations` (`station`) VALUES (%s)"
                        cursor.execute(sql, (station,))
                    elif row[0] == '/!!':
                        break
                    else:
                        code = row[0][:3]
                        sql = "UPDATE `stations` SET `code` = %s WHERE `station` = %s"
                        cursor.execute(sql, (code, stack[-1]))
                    print(count)
        connection.commit()
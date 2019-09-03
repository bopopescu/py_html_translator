from mysql.connector    import MySQLConnection, Error
import sys


def lang_field_connector(lang_str):
    langs_correct = {
        'uk': 'ua'
    }
    if (len(lang_str) > 0):
        if lang_str in langs_correct:
            return langs_correct[lang_str]
        else:
            return lang_str

#***********************************************************#
#------------ Проврка на существование перевода в БД --------------#
#***********************************************************#
def check_translates(db, user, password, lang_default = 'ru', values = []):
    if len(values) > 0 :
        try:
            prepare_values = []
            for item in values :
                prepare_values.append('"' + str(item) + '"')
            prepare_values = ','.join(prepare_values)
            # Connect
            db = MySQLConnection(host="localhost",
                                 user=user,
                                 passwd=password,
                                 db=db)
            if db.is_connected():
                c = db.cursor()
                c = db.cursor(buffered=True, dictionary=True)
                query = "SELECT * FROM modx_a_lang WHERE " + lang_default + " IN (" + prepare_values + ")"
                c.execute(query)
                translates = c.fetchall()
                c.close()

                if(translates) :
                    return translates
                else:
                    return []
            else:
                return []
        except Error as error:
            print(error)
        # finally:
        #     c.close()
    else :
        return []



#***********************************************************#
#------------ Добавление нового перевода в БД --------------#
#***********************************************************#
def add_translate(db, user, password, query):
    try:
        # Connect
        db = MySQLConnection(host="localhost",
                             user=user,
                             passwd=password,
                             db=db)

        if db.is_connected():
            print('Connected to MySQL database')

        c = db.cursor()

        # Execute SQL select statement
        if (query != ''):
            c.execute(query)
            db.commit()
            return c.lastrowid
        else:
            pass
    except Error as error:
        print(error)
    finally:
        c.close()
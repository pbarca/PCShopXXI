import psycopg2


class User:
    def __init__(self):
        self.reset()

    def reset(self):
        self.Id = None
        self.login = ''
        self.email = ''
        self.password = ''
        self.nif = ''
        self.nome = ''
        self.morada = ''

    def herokudb(self):
        from database import Database
        db = Database()
        return psycopg2.connect(host=db.Host, database=db.Database, user=db.User, password=db.Password,
                                sslmode='require')

    def gravar(self, login, email, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute(
            "CREATE TABLE IF NOT EXISTS usr (Id SERIAL NOT NULL,login text,email text, password text,nif text,nome text,morada CHAR(60))")
        db.execute("INSERT INTO usr VALUES (DEFAULT, %s, %s, %s)", (login, email, self.code(password),))
        ficheiro.commit()
        ficheiro.close()

    def existe(self, login):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM usr WHERE login = %s", (login,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def log(self, login, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE login = %s and password = %s", (login, self.code(password),))
        valor = db.fetchone()
        ficheiro.close()
        return valor

    def alterar(self, login, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("UPDATE usr SET password = %s WHERE login = %s", (self.code(password), login))
        ficheiro.commit()
        ficheiro.close()

    def apaga(self, login):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("DELETE FROM usr WHERE login = %s", (login,))
        ficheiro.commit()
        ficheiro.close()

    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select * from usr")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = None
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()

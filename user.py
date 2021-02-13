import psycopg2


class User:
    def __init__(self):
        self.reset()

    def reset(self):
        self.id = None
        self.cliente = ''
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

    def gravar(self, id, email, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
        db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (id, email, self.code(password)))
        ficheiro.commit()
        ficheiro.close()

    def existe(self, id):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("SELECT * FROM usr WHERE nome = %s", (id,))
            valor = db.fetchone()
            ficheiro.close()
        except:
            valor = None
        return valor

    def log(self, id, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (id, self.code(password),))
        valor = db.fetchone()
        ficheiro.close()
        return valor

    def alterar(self, id, password):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("UPDATE usr SET passe = %s WHERE nome = %s", (self.code(password), id))
        ficheiro.commit()
        ficheiro.close()

    def apaga(self, id):
        ficheiro = self.herokudb()
        db = ficheiro.cursor()
        db.execute("DELETE FROM usr WHERE nome = %s", (id,))
        ficheiro.commit()
        ficheiro.close()

    def lista(self):
        try:
            ficheiro = self.herokudb()
            db = ficheiro.cursor()
            db.execute("select * from usr ORDER BY nome")
            valor = db.fetchall()
            ficheiro.close()
        except:
            valor = None
        return valor

    @staticmethod
    def code(passe):
        import hashlib
        return hashlib.sha3_256(passe.encode()).hexdigest()

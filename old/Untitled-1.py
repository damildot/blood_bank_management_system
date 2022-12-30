""" in screen2 
    def save_to_table(self):
        try:
            data_tuple = (self.name, self.surname, self.inum, self.phone, self.gender,self.mail,self.birthdate,self.l_donation,self.b_group,self.weight,self.disease,self.adress,self.password)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            sqliteConnection.commit()
            print("Python Variables inserted successfully into SqliteDb_developers table")
            cursor.close()
        
except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed") """
from suds.client import Client

TCURL="https://tckimlik.nvi.gov.tr/Service/KPSPublic.asmx?WSDL"
client=Client(TCURL)
 
args={
    "TCKimlikNo":63208053636,
    "Ad":"furkan berk",
    "Soyad":"aydın",
    "DogumYili": 2000
}
 
print(client.service.TCKimlikNoDogrula(**args))
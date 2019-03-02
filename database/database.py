import sqlite3

# begin class TCDB()
class TCDB():
    # the following method initializes the tables 'acmw' and 'acmwsignin' in the database file
    def __init__(self):
        self.mConnection = sqlite3.connect("database/csuf-tcscanner.db")
        self.cursor = self.mConnection.cursor()

        self.createTableWithName("acmw")
        self.createTableWithName("acmwsignin")

    # the following method adds a person into the specified club in the database file
    def subscribePersonToClub(self, person, club='acmw'):
        dbcommand = "INSERT INTO "+club+" VALUES (?,?,?,?)"
        if type(person) is list:
            self.cursor.executemany(dbcommand, person)
        if type(person) is tuple:
            self.cursor.execute(dbcommand, person)
        self.mConnection.commit()
    
    # the following method removes a person from the the specified club in the database file
    def unsubscribePersonFromClub(self, person, club='acmw'):
        self.cursor.execute("DELETE FROM acmw WHERE CWID=(?)", (person[2],))
        self.mConnection.commit()

    # the following method checks if the person is subscribed to the specified club
    def isPersonSubscribedToClub(self, person, club='acmw'):
        self.cursor.execute("SELECT * FROM acmw WHERE CWID=(?)", (person[2],))
        data = self.cursor.fetchone()
        if not data:
            return False
        else:
            return True

    # the following method creates a table in the database
    def createTableWithName(self, tabletitle):
        dbcommand = "CREATE TABLE IF NOT EXISTS "+tabletitle+"(Name,TCID,CWID,Email)"
        self.cursor.execute(dbcommand)
        self.mConnection.commit()
    
    # the following method deletes a table in the database
    def deleteTableWithName(self, tabletitle):
        dbcommand = "DROP TABLE "+tabletitle
        self.cursor.execute(dbcommand)
        self.mConnection.commit()
# end class TCDB()

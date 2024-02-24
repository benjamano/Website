import datetime, sqlite3

from flask import Flask, render_template, redirect, request, url_for, session, flash

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = "rfwef65657eo234w223fh33HI2UhuhgR7YG"

sql = sqlite3.connect("/home/BenMercer/backend/Parties.db", check_same_thread=False)
q = sql.cursor()

def onStart():
    try:
        
        tblRoom = "CREATE TABLE IF NOT EXISTS Room (RoomID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Capacity INT NOT NULL)"
        
        tblPartyType = "CREATE TABLE IF NOT EXISTS PartyType (PartyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Price per Child DECIMAL(5,2) NOT NULL, Price per Adult DECIMAL(5,2) NOT NULL, Duration INTEGER NOT NULL, LasertagTime TIME))"

        tblParties = "CREATE TABLE IF NOT EXISTS Parties (PartyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, FoodOrderID INTEGET NOT NULL, PartyType TEXT NOT NULL, RoomID INTEGER NOT NULL, Date DATE NOT NULL, Time TIME NOT NULL, BookedAdults INT NOT NULL, BookedChildren INT NOT NULL, FirstChildName TEXT NOT NULL, SecondChildName TEXT, FOREIGN KEY (PartyType) REFERENCES PartyType(PartyType)) FOREIGN KEY (RoomID) REFERENCES Room(RoomID), FOREIGN KEY (FoodOrderID) REFERENCES PartyFoodOrder(FoodOrderID)"
        
        tblFood = "CREATE TABLE IS NOT EXISTS Food (FoodID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL)"
        
        tblFoodOrder = "CREATE TABLE IF NOT EXISTS PartyFoodOrder (FoodOrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, PartyID INTEGER NOT NULL, FoodID INTEGER NOT NULL, Quantity INT NOT NULL, FOREIGN KEY (PartyID) REFERENCES Parties(PartyID), FOREIGN KEY (FoodID) REFERENCES Food(FoodID))"

        q.execute(tblRoom)
        q.execute(tblPartyType)
        q.execute(tblParty)
        q.execute(tblFood)
        q.execute(tblFoodOrder)

    except Exception as error:
        app.logger.info(f"Error while creating tables: {error}")


onStart()


@app.route("/")
def home():
    
    return render_template("index.html")

@app.route("/projects")
def laserTag():
    
    return render_template("projects.html")

@app.route("/login", methods = ['GET', 'POST'])
def login():
    
    if request.method == "POST":
    
        username = request.form["username"]
        password = request.form["password"]
        
        if username == "ben" and password == "B3n1sCool":
            session["loggedin"] = True
            return redirect(url_for("partyHome"))
        
        else:
            flash("Invalid username or password")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    
    session["loggedin"] = False
    
    return redirect(url_for("home"))

@app.route("/partyhome", methods = ['GET', 'POST'])
def partyHome():
    
    if session["loggedin"] == False:
        return redirect(url_for("login"))
    
    else:
        return render_template("/system/home.html", time=int(datetime.datetime.now().strftime("%H")))
    
@app.route("/new", methods = ['GET', 'POST'])
def newParty():
    
    
    addroom = "INSERT INTO Room (Name, Capacity) VALUES (?, ?)"
    q.execute(addroom, ["Room 1", 20])
    
    q.execute(addroom, ["Room 2", 35])
        
    
    if session["loggedin"] == False:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        
        partytype = request.form["PartyType"]
        firstchildname = request.form["FirstChildName"]
        secondchildname = request.form["SecondChildName"]
        childnum = request.form["NumChildren"]
        age = request.form["Age"]
        
        parties = "SELECT BookedChildren, PartyID FROM Parties ORDER BY BookedChildren DESC WHERE Date = ? AND Time = ?"
        
        try:
            q.execute(parties, ["24/02/2024", "15:00"])
            
            if largestparty[0] < childnum:
                Room = 2
            else:
                Room = 1
                editParty = "UPDATE Parties SET RoomID = 1 WHERE PartyID = ?"
            
            q.execute(editParty, [largestparty[1]])
            
            largestparty = q.fetchone()
        
        except Exception as error:
            app.logger.info(f"Error while getting largest party: {error}")
            Room = 2
        
        createParty = "INSERT INTO Parties (PartyTypeID, RoomID, Date, Time, BookedAdults, BookedChildren) VALUES (?, ?, ?, ?, ?, ?)"
        q.execute(createParty, [partytype, Room, "24/02/2024", "15:00", 0, childnum])
        
        flash(f"{partytype}, {firstchildname}, {secondchildname}, {childnum}, {age}, {largestparty[0]}, {Room}")
        
        return render_template("/system/newparty.html")
            
    else:
        return render_template("/system/newparty.html")

@app.route("/modify", methods = ['GET', 'POST'])
def modifyParty():
    
    if session["loggedin"] == False:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        
        partyid = request.form.get("PartyID")
        date = request.form.get("Date")
        time = request.form.get("Time")
        partytype = request.form.get("PartyType")
        firstchildname = request.form.get("FirstChildName")
        secondchildname = request.form.get("SecondChildName")
        age = request.form.get("Age")
        
        search_query = "SELECT * FROM Parties WHERE "
        search_params = []
        
        if partyid:
            search_query += "PartyID = ? AND "
            search_params.append(partyid)
        
        if date:
            search_query += "Date = ? AND "
            search_params.append(date)
        
        if time:
            search_query += "Time = ? AND "
            search_params.append(time)
        
        if partytype:
            search_query += "PartyType = ? AND "
            search_params.append(partytype)
        
        if firstchildname:
            search_query += "FirstChildName = ? AND "
            search_params.append(firstchildname)
        
        if secondchildname:
            search_query += "SecondChildName = ? AND "
            search_params.append(secondchildname)
        
        if age:
            search_query += "Age = ? AND "
            search_params.append(age)
        
        search_query = search_query.rstrip("AND ")
    
        q.execute(search_query, search_params)
        
        parties = q.fetchall()
        
        return render_template("/system/modifyparty.html", parties=parties)
        
    else:
        return render_template("/system/modifyparty.html")

if __name__ == '__main__':
    app.run()
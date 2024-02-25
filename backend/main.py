import datetime, sqlite3

from flask import Flask, render_template, redirect, request, url_for, session, flash

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = "rfwef65657eo234w223fh33HI2UhuhgR7YG"

sql = sqlite3.connect("/home/BenMercer/backend/Parties.db", check_same_thread=False)
q = sql.cursor()

def onStart():
    try:
        
        tblRoom = "CREATE TABLE IF NOT EXISTS Room (RoomID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, Capacity INT NOT NULL)"

        tblPartyType = "CREATE TABLE IF NOT EXISTS PartyType (PartyTypeID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL, PriceChild DECIMAL(5,2) NOT NULL, PriceAdult DECIMAL(5,2) NOT NULL, Duration INTEGER NOT NULL)"

        tblParties = "CREATE TABLE IF NOT EXISTS Parties (PartyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, FoodOrderID INTEGER, PartyTypeID INT NOT NULL, RoomID INTEGER NOT NULL, Date DATE NOT NULL, Time TIME NOT NULL, BookedChildren INT NOT NULL, FirstChildName TEXT NOT NULL, SecondChildName TEXT, LasertagTime TEXT, FOREIGN KEY (PartyTypeID) REFERENCES PartyType(PartyTypeID), FOREIGN KEY (RoomID) REFERENCES Room(RoomID), FOREIGN KEY (FoodOrderID) REFERENCES PartyFoodOrder(FoodOrderID))"

        tblFood = "CREATE TABLE IF NOT EXISTS Food (FoodID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL)"

        tblSide = "CREATE TABLE IF NOT EXISTS Side (SideID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Name TEXT NOT NULL)"

        tblFoodOrder = "CREATE TABLE IF NOT EXISTS PartyFoodOrder (FoodOrderID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, PartyID INTEGER NOT NULL, FoodID INTEGER NOT NULL, SideID INTEGER NOT NULL, Quantity INT NOT NULL, FOREIGN KEY (PartyID) REFERENCES Parties(PartyID), FOREIGN KEY (FoodID) REFERENCES Food(FoodID), FOREIGN KEY (SideID) REFERENCES Side(SideID))"

        q.execute(tblRoom)
        q.execute(tblSide)
        q.execute(tblFood)
        q.execute(tblFoodOrder)
        q.execute(tblParties)
        q.execute(tblPartyType)
        
        
        # addrooms = "INSERT INTO Room (Name, Capacity) VALUES (?, ?)"
        # q.execute(addrooms, ["Room 1", 20])
        # q.execute(addrooms, ["Room 2", 35])
        
        # addside = "INSERT INTO Side (Name) VALUES (?)"
        # q.execute(addside, ["Beans"])
        # q.execute(addside, ["Peas"])
        # q.execute(addside, ["Sweetcorn"])
        
        # addfood = "INSERT INTO Food (Name) VALUES (?)"
        # q.execute(addfood, ["Sausage"])
        # q.execute(addfood, ["Nuggets"])
        # q.execute(addfood, ["Burger"])
        # q.execute(addfood, ["FishFingers"])
        # q.execute(addfood, ["GFSausage"])
        
        # sql.commit()
        
        
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
    
    if session["loggedin"] == False:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        
        partytype = request.form["PartyType"]
        firstchildname = request.form["FirstChildName"]
        secondchildname = request.form["SecondChildName"]
        childnum = request.form["NumChildren"]
        age = request.form["Age"]
        time= request.form["PartyTime"]
        largestparty = []
        date = session["date"]
        
        
        app.logger.info(f"Party type: {partytype}, First child: {firstchildname}, Second child: {secondchildname}, Number of children: {childnum}, Age: {age}, Time: {time}")
        
        parties = "SELECT BookedChildren, PartyID FROM Parties WHERE Date = ? AND Time = ? ORDER BY BookedChildren DESC"
        
        try:
            q.execute(parties, [date, time])
            
            largestparty = q.fetchone()
            
            if largestparty[0] < childnum:
                Room = 2
            else:
                Room = 1
                
                editParty = "UPDATE Parties SET RoomID = 1 WHERE PartyID = ?"
                
                q.execute(editParty, [largestparty[1]])
                
                sql.commit()
        
        except Exception as error:
            app.logger.info(f"Error while getting largest party: {error}")
            Room = 2
        
        createParty = "INSERT INTO Parties (PartyTypeID, FirstChildName, RoomID, Date, Time, BookedChildren) VALUES (?, ?, ?, ?, ?, ?)"
        q.execute(createParty, [partytype, firstchildname, Room, date, time, childnum])
        
        sql.commit()
        
        flash(f"{partytype}, {firstchildname}, {secondchildname}, {childnum}, {age}, {largestparty}, {Room}")
        
        return redirect(url_for("partyHome"))
            
    else:
        
        date = session["date"]
        
        partyexists = "SELECT Count(*) FROM Parties WHERE Date = ? AND PartyTypeID = ? AND Time = ?"
        
        max_parties = {1: 2, 3: 2, 5: 2, 2: 1, 4: 1, 6: 1}
        
        isopen = {}
        
        times = ["10:30", "11:30", "15:00", "16:00"]
        
        for i in range(1, 7):
            isopen[i] = {}
            for time in times:
                q.execute(partyexists, [date, i, time])
                noofparties = q.fetchall()
                if noofparties[0][0] <= max_parties[i]:
                    isopen[i][time] = True
                else:
                    isopen[i][time] = False

        app.logger.info(f"\n\nIs open: {isopen}\n\n{isopen[1]['10:30']}\n\n{isopen[5]['16:00']}")

        return render_template("/system/newparty.html", isopen = isopen)

    
@app.route("/newdate", methods = ['GET', 'POST'])
def newPartyDate():
    
    if request.method == "POST":
        
        date = request.form["PartyDate"]
        session["date"] = date
        
        if date:
        
            return redirect(url_for("newParty"))
        
        else:
            flash("Please enter a date")
            
    return render_template("/system/newpartydate.html")
    
    
@app.route("/modify", methods = ['GET', 'POST'])
def modifyParty():
    
    if session["loggedin"] == False:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        
        partyid = request.form["PartyID"]
        date = request.form["PartyDate"]
        time = request.form["PartyTime"]
        #partytype = request.form["PartyType"]
        firstchildname = request.form["FirstName"]
        secondchildname = request.form["SecondName"]
        age = request.form["Age"]
        
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
        
        #if partytype:
            #search_query += "PartyType = ? AND "
            #search_params.append(partytype)
        
        if firstchildname:
            search_query += "FirstChildName = ? AND "
            search_params.append(firstchildname)
        
        if secondchildname:
            search_query += "SecondChildName = ? AND "
            search_params.append(secondchildname)
        
        if age:
            search_query += "Age = ? AND "
            search_params.append(age)
            
        if not age and not firstchildname and not time and not date and not partyid:
            app.logger.info("No search parameters entered")
            flash("Please enter a value for atleast one field")
        
        search_query = search_query.rstrip("AND ")
        
        app.logger.info(f"Search query: {search_query}, ({search_params})")
    
        q.execute(search_query, search_params)
        
        parties = q.fetchall()
        
        return render_template("/system/modifyparty.html", parties=parties)
        
    else:
        return render_template("/system/modifyparty.html")

if __name__ == '__main__':
    app.run()
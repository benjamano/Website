import datetime, sqlite3, requests, uuid
import threading

from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify

from odsclient import get_whole_dataset
import random
import string
import schedule
import time

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = "rfwef65657eo234w223fh33HI2UhuhgR7YG"

try:

    sql = sqlite3.connect("/home/BenMercer/backend/Parties.db", check_same_thread=False)
    
    q = sql.cursor()

except Exception as error:
    app.logger.info(f"Error while connecting to database: {error}")

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

def fetchApiData(mode):
    url = "https://ukpowernetworks.opendatasoft.com/api/explore/v2.1/catalog/datasets/"
    apikey = "2444be3184703156aa82afb58a6e9d1cdbe7e1b75b588d3329637c24"
    headers = { "Content-Type": "application/json",
                "Authorization": f"Apikey {apikey}" }
    
    if mode == "faults":
        url += f"ukpn-live-faults/records"
    
    elif mode == "lct":
        url += f"low-carbon-technologies/records?where=type%20%3D%20%22Wind%22&limit=100"
        
    with requests.get(url, headers=headers) as response:
        if response.status_code == 200:
            return response.json()
        else:
            app.logger.info(f"Failed to retrieve data. Status code: {response.status_code}")
            return {"error": "Failed to retrieve data"}

@app.route("/getfaultdata")
def faultdataapi():
    try:

        response = fetchApiData("faults")
        
        return jsonify(response["results"])  
    
    except Exception as error:
        app.logger.info("Error while getting data:", error)
        return jsonify({"error": str(error)})
    
@app.route("/getlctdata")
# Low carbon
def energylctapi():
    try:
        response = fetchApiData("lct")
        
        return jsonify(response["results"])  
    
    except Exception as error:
        app.logger.info("Error while getting data:", error)
        return jsonify({"error": str(error)})

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
            
            if int(largestparty[0]) < int(childnum):
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
        
        partyexists = "SELECT Count() FROM Parties WHERE Date = ? AND PartyTypeID = ? AND Time = ?"
        
        max_parties = {1: 2, 3: 2, 5: 2, 2: 1, 4: 1, 6: 1}
        
        isopen = {}
        
        times = ["10:30", "11:30", "15:00", "16:00"]
        
        for i in range(1, 7):
            isopen[i] = {}
            for time in times:
                q.execute(partyexists, [date, i, time])
                noofparties = q.fetchone()[0]
                app.logger.info(f"Party type: {i}, Time: {time}, No of parties: {noofparties}, Max parties: {max_parties[i]}, date: {date}")
                if noofparties <= max_parties[i]:
                    isopen[i][time] = True
                else:
                    isopen[i][time] = False

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
            flash("Please enter a value for atleast one field")
        
        search_query = search_query.rstrip("AND ")
        
        #app.logger.info(f"Search query: {search_query}, ({search_params})")
    
        q.execute(search_query, search_params)
        
        parties = q.fetchall()
        
        return render_template("/system/modifyparty.html", parties=parties)
        
    else:
        return render_template("/system/modifyparty.html")
    
    
    
# ------------------------------------------------- ICT WEBSITE ------------------------------------------------- #

@app.route("/hotbeanshome")
def hotbeanshome():
    
    return render_template("/ICTWebsite/ICTHome.html")

@app.route("/hotbeanscareers")
def hotbeanscareers():
    
    return render_template("/ICTWebsite/ICTCareers.html")

@app.route("/hotbeanscontact")
def hotbeanscontact():
    
    return render_template("/ICTWebsite/ICTContact.html")

@app.route("/hotbeansportfolio")
def hotbeansportfolio():
    
    return render_template("/ICTWebsite/ICTPortfolio.html")

@app.route("/hotbeansservice")
def hotbeansservice():
    
    return render_template("/ICTWebsite/ICTService.html")    

# ------------------------------------------------- TESTING    ------------------------------------------------- #

@app.route("/verify")
def verify():
    
    with open("backend\dailyPassPhrase.txt", "r") as f:
        pCode = f.read()
    
    return render_template("verify.html", pCode=pCode)

@app.route('/verifycode=<code>', methods=['GET'])
def verify_code(code):
    if not code:
        return jsonify({'error': 'Passphrase not provided'}), 400
    
    with open("backend\dailyPassPhrase.txt", "r") as f:
        passphrase = f.read()
    
        if code == passphrase:
            return jsonify({'result': 'yes'})
        else:
            return jsonify({'result': 'no'})

def daily_task():
    
    with open("backend\dailyPassPhrase.txt", "w") as f:
        
        letters = string.ascii_lowercase
        pCode = ''.join(random.choice(letters) for i in range(5))
        
        f.write(pCode)
        
        f.close()

if __name__ == '__main__':
    onStart()
    schedule.every().day.at("22:58").do(daily_task)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    app.run()
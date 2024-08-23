from ctypes import pythonapi
import datetime, sqlite3, requests, uuid
import threading

from flask import Flask, render_template, redirect, request, url_for, session, flash, jsonify

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from odsclient import get_whole_dataset
import random
import string
import schedule
import time
from urllib.parse import parse_qs

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app.secret_key = "rfwef65657eo234w223fh33HI2UhuhgR7YG"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lme.db'
db = SQLAlchemy(app)

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


# -------------------------------------------------  Life Maker-Easier  ------------------------------------------------- #

@app.route("/lme")
def lme():
    with app.app_context():
        db.create_all()
    if 'loggedIntoLME' not in session or session['loggedIntoLME'] == False:
        return redirect(url_for('lme_login'))

    return render_template("/lifemakereasier/index.html")

@app.route("/lme/login", methods = ['GET', 'POST'])
def lme_login():
    if 'loggedIntoLME' in session and session['loggedIntoLME'] == True:
        return redirect(url_for('lme'))


    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username.title() == 'Ben' and password == 'B3n1sCool':
            session['loggedIntoLME'] = True
            return redirect(url_for('lme'))

        else:
            flash('Invalid username or password')

    return render_template("/lifemakereasier/login.html")

@app.route("/lme/logout")
def lme_logout():
    session['loggedIntoLME'] = False
    return redirect(url_for('lme_login'))

@app.route("/lme/money")
def lme_money():
    if 'loggedIntoLME' not in session or session['loggedIntoLME'] == False:
        return redirect(url_for('lme_login'))

    return render_template("/lifemakereasier/money.html")

@app.route("/lme/settings")
def lme_settings():
    if 'loggedIntoLME' not in session or session['loggedIntoLME'] == False:
        return redirect(url_for('lme_login'))

    return render_template("/lifemakereasier/settings.html")

# ------------------------------------------------- API ---------------------------------------------------------#

@app.route("/api/logShift", methods = ['POST', 'GET'])
def logShift():
    raw_data = request.data.decode('utf-8')
    parsed_data = parse_qs(raw_data)

    date = parsed_data.get('date', [None])[0]
    startTime = parsed_data.get('startTime', [None])[0]
    endTime = parsed_data.get('endTime', [None])[0]
    breakTime = parsed_data.get('breakTime', [None])[0]

    if not date or not startTime or not endTime or not breakTime:
        return jsonify({'error': 'Missing parameters'}), 400

    existingShift = Shifts.query.filter(Shifts.date == date).all()

    if len(existingShift) > 0:

        return jsonify({'error': 'Shift already exists'}), 400

    shift = Shifts(date=date, startTime=startTime, endTime=endTime, breakTime=breakTime)

    db.session.add(shift)

    db.session.commit()

    return jsonify({'result': 'yes'})

@app.route("/api/getShifts", methods = ['GET'])
def getShifts():

        shifts = Shifts.query.all()

        shiftList = []

        for shift in shifts:
            shiftList.append({'date': shift.date, 'startTime': shift.startTime, 'endTime': shift.endTime, 'breakTime': shift.breakTime})

        return jsonify(shiftList)

@app.route("/api/logExpense", methods = ['POST'])
def logExpense():
    raw_data = request.data.decode('utf-8')
    parsed_data = parse_qs(raw_data)

    reason = parsed_data.get('reason', [None])[0]
    date = parsed_data.get('date', [None])[0]
    amount = parsed_data.get('amount', [None])[0]
    description = parsed_data.get('description', [None])[0]

    if not date or not amount or not description:
        return jsonify({'error': 'Missing parameters'}), 400

    newExpense = Expenses(reason=reason, date=date, amount=amount, description=description)

    db.session.add(newExpense)

    db.session.commit()

    return jsonify({'result': 'yes'})

@app.route("/api/createNewLink", methods = ['GET', 'POST'])
def createNewLink():
    
    URLName = request.args.get('linkName')
    #app.logger.info(URLName)

    
    if URLName:
        newLink = f"https://benmercer.pythonanywhere.com/redirect={URLName}"
    else:
        return jsonify({"error": "linkName parameter is missing"}), 400
        
    return jsonify({"newLink": newLink})

@app.route("/api/addNewURL", methods = ['GET', 'POST'])
def addNewURL():

    linkURL = URLName = request.args.get('linkURL')
    description = URLName = request.args.get('description')

    newLink = LinkClicks(linkUrl = linkURL, description=description, noClicks=0)

    db.session.add(newLink)

    db.session.commit()

    return jsonify({'result': 'yes'})

@app.route("/api/getLinks", methods = ['GET'])
def getLinks():
    links = LinkClicks.query.all()

    linkList = []

    for link in links:
        linkList.append({'Id': link.id, 'url': link.linkUrl, 'noClicks': link.noClicks, 'isActive': link.isActive})

    return jsonify(linkList)
    
@app.route("/redirect=<URLName>", methods=['GET'])
def redirectURL(URLName):
    if URLName:
        try:
            URLName = f"https://benmercer.pythonanywhere.com/redirect{URLName}"
        
            link = LinkClicks.query.filter_by(linkUrl=URLName).first()
            
            if len(link) > 1:
                link.noClicks = (link.noClicks or 0) + 1
                db.session.commit()
                
        except:
            pass

    
    return redirect(url_for(home))
    
# ------------------------------------------------- TESTING    ------------------------------------------------- #

@app.route("/verify")
def verify():

    with open("backend/dailyPassPhrase.txt", "r") as f:
        pCode = f.read()

    return render_template("verify.html", pCode=pCode)

@app.route('/verifycode=<code>', methods=['GET'])
def verify_code(code):
    if not code:
        return jsonify({'error': 'Passphrase not provided'}), 400

    with open("backend/dailyPassPhrase.txt", "r") as f:
        passphrase = f.read()

        if code == passphrase:
            return jsonify({'result': 'yes'})
        else:
            return jsonify({'result': 'no'})

def daily_task():

    with open("backend/dailyPassPhrase.txt", "w") as f:

        letters = string.ascii_lowercase
        pCode = ''.join(random.choice(letters) for i in range(5))

        f.write(pCode)

        f.close()

#------------------------- | SQL Alchemy CLASSES |--------------------------#




class Shifts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    startTime = db.Column(db.String(5), nullable=False)
    endTime = db.Column(db.String(5), nullable=False)
    breakTime = db.Column(db.String(5), nullable=False)
    isActive = db.Column(db.Boolean, default=True)



class Jobs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    salary = db.Column(db.String(20), nullable=True)
    hourlyRate = db.Column(db.String(20), nullable=False)
    isActive = db.Column(db.Boolean, default=True)


class PassedHourlyRates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hourlyRate = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    jobId = db.Column(db.Integer, db.ForeignKey('jobs.id'))
    job = db.relationship('Jobs', backref='passedHourlyRate')


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reason = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=True)
    isActive = db.Column(db.Boolean, default=True)


class LinkClicks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    linkUrl =  db.Column(db.String(500), nullable=False)
    noClicks = db.Column(db.Integer, nullable=True)
    description =  db.Column(db.String(100), nullable=False)
    isActive = db.Column(db.Boolean, default=True)


#End of SQL Alchemy Classes




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


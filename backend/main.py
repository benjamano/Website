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

        tblParty = "CREATE TABLE IF NOT EXISTS Parties (PartyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, FoodOrderID INTEGET NOT NULL, PartyTypeID INTEGER NOT NULL, RoomID INTEGER NOT NULL, Date DATE NOT NULL, Time TIME NOT NULL, BookedAdults INT NOT NULL, BookedChildren INTO NOT NULL, FOREIGN KEY (PartyTypeID) REFERENCES PartyType(PartyTypeID)) FOREIGN KEY (RoomID) REFERENCES Room(RoomID), FOREIGN KEY (FoodOrderID) REFERENCES PartyFoodOrder(FoodOrderID)"
        
        tblPartyFoodOrder = "CREATE TABLE IF NOT EXISTS PartyFoodOrder (FoodOrderID INTERGER NOT NULL AUTOINCREMENT, PartyID INTEGER NOT NULL, Sausage INT NOT NULL, SausageP INT NOT NULL, SausageS INT NOT NULL, SausageB INT NOT NULL, Chicken INT NOT NULL, ChickenP INT NOT NULL, ChickenS INT NOT NULL, ChickenB INT NOT NULL, Fish INT NOT NULL, FishP INT NOT NULL, FishP INT NOT NULL, FishB INT NOT NULL, GFSausageP INT NOT NULL, GFSausageS INT NOT NULL, GFSausageB INT NOT NULL, FOREIGN KEY (PartyID) REFERENCES Party(PartyID))"

        q.execute(tblRoom)
        q.execute(tblPartyType)
        q.execute(tblParty)
        q.execute(tblPartyFoodOrder)

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
            return redirect(url_for("partyhome"))
        
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
        return render_template("/system/home.html", time=datetime.datetime.now().strftime("%H"))
    
@app.route("/partyhome/new", methods = ['GET', 'POST'])
def newParty():
    
    if session["loggedin"] == False:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        
        partytype = request.form["PartyType"]
        childname = ("'"+{request.form["FirstChildName"]}+"'", "'"+{request.form["SecondChildName"]}+"'")
        childnum = request.form["NumChildren"]
        age = request.form["Age"]
        
        flash(f"{partytype}, {childname}, {childnum}, {age}")
            
    else:
        return render_template("/system/new.html")

if __name__ == '__main__':
    app.run()
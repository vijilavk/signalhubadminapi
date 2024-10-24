from flask import *
import pymysql as pymysql

flow= Flask(__name__)
flow.secret_key = "abc"
con = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="smartflow", charset="utf8")
cmd = con.cursor()


@flow.route('/')
def login():
    return render_template("login.html")
@flow.route('/logincheck', methods=['post'])
def logincheck():
    user = request.form['username']
    psd = request.form['password']
    cmd.execute("select * from `login` where email='" + user + "' and password='" + psd + "'")
    result = cmd.fetchone()
    if result is None:
        return '''<script>alert("INVALID USERNAME AND PASSWORD");window.location='/'</script>'''
    elif result[3] == "admin":
        session['lid'] = result[0]
        return render_template('home.html')
@flow.route('/users')
def users():
    return render_template("users.html")

@flow.route('/viewuser')
def viewuser():
    cmd.execute("select userreg.*,login.type from `userreg` join login on  login.`login_id`=`userreg`.`login_id` where login.type='user' or login.type='emergency'")
    result=cmd.fetchall()
    return render_template("view_user.html",value=result)

@flow.route('/viewnewrequest')
def viewnewrequest():
    cmd.execute("select userreg.*,login.type from `userreg` join login on  login.`login_id`=`userreg`.`login_id` where login.type='pending' ")
    result=cmd.fetchall()
    return render_template("newrequest.html",value=result)
@flow.route('/viewrejecteduser')
def viewrejecteduser():
    cmd.execute("select userreg.*,login.type from `userreg` join login on  login.`login_id`=`userreg`.`login_id` where login.type='rejected' ")
    result=cmd.fetchall()
    return render_template("rejecteduserview.html",value=result)
@flow.route('/newrequestconfirm')
def newrequestconfirm():
    usertype = request.args.get("type")
    loginid = request.args.get("id")
    print(usertype)
    print(loginid)
    session['type']=usertype
    session['id']=loginid
    return render_template("newrequestconfirm.html")
@flow.route('/acceptuser',methods=['post'])
def acceptuser():
    usertype=session["type"]
    loginid=session["id"]
    cmd.execute("UPDATE login JOIN userreg ON login.`login_id`=`userreg`.`login_id` SET login.`type`='"+usertype+"' WHERE userreg.`usertype`='"+usertype+"' AND `login`.`login_id`='"+loginid+"' ")
    con.commit()
    return "success"
@flow.route('/rejectuser',methods=['post'])
def rejectuser():

    loginid=session["id"]
    cmd.execute("UPDATE login JOIN userreg ON login.`login_id`=`userreg`.`login_id` SET login.`type`='rejected'  WHERE  `login`.`login_id`='"+loginid+"'")
    con.commit()
    return '''<script>alert("UPDATED SUCCESSFULLY");window.location='/signup'</script>'''
@flow.route('/viewtraffic')
def viewtraffic():
    cmd.execute("""
    SELECT `trafficcontrol`.*, `userreg`.* 
    FROM `trafficcontrol` 
    JOIN `userreg` 
        ON `trafficcontrol`.`login_id` = `userreg`.`login_id` 
    WHERE CONCAT(`trafficcontrol`.`date`, ' ', `trafficcontrol`.`time`) <= NOW() 
    ORDER BY `trafficcontrol`.`date` DESC, `trafficcontrol`.`time` DESC
""")
    res=cmd.fetchall()
    return render_template("viewtrafficcontrol.html",value=res)
@flow.route('/viewcongestion')
def viewcongestion():
    cmd.execute("SELECT `congestion`.* FROM `congestion`")
    result=cmd.fetchall()
    return render_template("viewcongestion.html",value=result)
@flow.route('/suggestroute')
def suggestroute():
    conid=request.args.get("conid")
    session["congestionid"]=conid
    return render_template("suggestroute.html")
@flow.route('/updateroute',methods=['post'])
def updateroute():

    conid=session["congestionid"]
    route=request.form["sroute"]
    cmd.execute("update congestion set suggested_route='"+route+"' where congestion_id='"+conid+"'")
    con.commit()
    return "success"
@flow.route('/alert')
def alert():
    cmd.execute("SELECT `alert`.*,`userreg`.* FROM `alert` JOIN `userreg` ON `alert`.`loginid`=`userreg`.`login_id` ORDER BY `alert`.date DESC")
    res=cmd.fetchall()

    return render_template("alert.html",value=res)



flow.run(debug=True)

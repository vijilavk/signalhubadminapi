from flask import *
# from datetime import datetime
import pymysql
# import threading
# from flask import Flask, request, jsonify
# import cv2
# import numpy as np
import pymysql

# res = "none"
# ress = "none"
# flag_c = 0
#
# # Load YOLOv3 weights and configuration
# net = cv2.dnn.readNet("C:\\Users\\VYSHAK\\PycharmProjects\\smartflow\\yolov3.weights", "C:\\Users\\VYSHAK\\PycharmProjects\\smartflow\\yolov3.cfg")
# classes = []
# with open("C:\\Users\\VYSHAK\\PycharmProjects\\smartflow\\coco.names", "r") as f:
#     classes = [line.strip() for line in f.readlines()]
#
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
# # Indexes of vehicle classes in COCO dataset
# vehicle_class_ids = [classes.index(cls) for cls in ['car', 'truck', 'bus', 'motorbike', 'bicycle']]


flow = Flask(__name__)

con = pymysql.connect(host='localhost',user='root',password='root',db='smartflow',charset='utf8')
cmd = con.cursor()

@flow.route("/userregister",methods=['get','post'])
def userregister():
    name = request.form.get("username")
    phone = request.form.get("phone")
    email = request.form.get("email")
    rc = request.form.get("rc_number")
    adhr=request.form.get("adhaar_number")
    password = request.form.get("password")
    print(name)
    print(phone)
    print(email)
    print(rc)
    print(adhr)
    print(password)
    cmd.execute("select * from user_registration where `rc_number`='"+rc+"' or adhaar_number='"+adhr+"' or email='"+email+"' or phone='"+phone+"'")
    res=cmd.fetchone()
    print("res",res)
    if res==None:
       cmd.execute("insert into login values(null,'"+email+"','"+password+"','user','pending')")
       con.commit()
       loginid = cmd.lastrowid
       print(loginid)
       cmd.execute("INSERT INTO `user_registration` VALUES(NULL,'"+name+"','"+str(phone)+"','"+email+"','"+rc+"','"+str(loginid)+"','"+adhr+"')")
       con.commit()
       return jsonify({'task': "successfully inserted"})

    else:
        return jsonify({'task': "already existed"})

@flow.route("/logincheck",methods=['get','post'])
def logincheck():
    email = request.args.get("email")
    passwrd = request.args.get("password")
    cmd.execute("select * from login where email='"+email+"' and password='"+passwrd+"'")
    result = cmd.fetchone()
    print(result)
    if result is None:
        return jsonify({'task': "invalid"})
    elif result[3] == 'user':
        return jsonify({'task': "success",'loginid': result[0],'type':result[3],'status':result[4]})
    elif result[3] == 'admin':
        return jsonify({'task':"success",'loginid':result[0],'type':result[3],'status':result[4]})

# @flow.route("/viewallusers",methods=['get','post'])
# def viewallusers():
#     cmd.execute("select `login`.*,`user_registration`.* from `login` join `user_registration` on `login`.`login_id`=`user_registration`.`login_id` where `login`.`status`='accepted'")
#     s=cmd.fetchall()
#     header=[x[0] for x in cmd.description]
#     json_data=[]
#     for result in s:
#         json_data.append(dict(zip(header,result)))
#     print(json_data)
#     return jsonify(json_data)

@flow.route("/selectuser",methods=['get','post'])
def selectuser():
    id=request.args.get("login_id")
    print(id)
    cmd.execute("SELECT * FROM `user_registration` WHERE `login_id`='"+id+"'")
    s=cmd.fetchone()
    print(s)
    header=[x[0] for x in cmd.description]
    json_data=[]
    if s:
        json_data.append(dict(zip(header, s)))
        print(json_data)
    return jsonify(json_data)

@flow.route("/edituser",methods=['get','post'])
def edituser():
    logid = request.form.get("login_id")
    name = request.form.get("username")
    phn = request.form.get("phone")
    email = request.form.get("email")
    passwrd = request.form.get("password")
    rc = request.form.get("rc_number")
    adhr = request.form.get("adhaar_number")
    cmd.execute("update user_register set username='"+name+"',phone='"+phn+"',email='"+email+"',password='"+passwrd+"',rc='"+rc+"',adhaar_number='"+adhr+"',where login_id='"+logid+"'")
    con.commit()
    return jsonify({'task':"success"})

@flow.route("/deleteuser",methods=['get','post'])
def deleteuser():
    logid = request.args.get("login_id")
    cmd.execute("delete from user_registration where login_id='"+str(logid)+"'")
    con.commit()
    cmd.execute("DELETE FROM `login` WHERE `login_id`='"+str(logid)+"'")
    con.commit()
    return jsonify({'task':"success"})


# @flow.route('/showpendingusers',methods=['get','post'])
# def showpendingusers():
#     # loginid=request.args.get("loginid")
#     cmd.execute(
#         "select `login`.*,`user_registration`.* from `login` join `user_registration` on `login`.`login_id`=`user_registration`.`login_id` where `login`.`status`='pending'")
#     s = cmd.fetchall()
#     header = [x[0] for x in cmd.description]
#     json_data = []
#     for result in s:
#         json_data.append(dict(zip(header, result)))
#     print(json_data)
#     return jsonify(json_data)

    # cmd.execute("SELECT * FROM login WHERE status = 'pending'")
    # pending_users = cmd.fetchall()
    # con.commit()
    # return jsonify({'status': 'success', 'users': pending_users})
    # return jsonify({'task': "success"})


@flow.route("/congestion_alerts",methods=['get','post'])
def congestion_alerts():
    cmd.execute("SELECT * FROM `alerts` where alert_type='congestion'")
    # return jsonify({'task': "success"})
    s = cmd.fetchall()
    header = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(header, result)))
        print(json_data)
    return jsonify(json_data)

@flow.route("/user_profile",methods=['get','post'])
def user_profile():
    logid = request.args.get("login_id")
    print(logid)
    cmd.execute("select * from user_registration where login_id='"+str(logid)+"'")
    s = cmd.fetchone()
    print(s)
    header = [x[0] for x in cmd.description]
    json_data = []
    if s:
        json_data.append(dict(zip(header, s)))
        print(json_data)
    return jsonify(json_data)

@flow.route("/changepassword",methods=['get','post'])
def changepassword():
    oldpassword = request.args.get("oldpassword")
    newpassword = request.args.get("newpassword")
    cmd.execute("select * from login where password='"+oldpassword+"'")
    result = cmd.fetchone()
    if result is None:
        return jsonify({'task': "Invalid"})
    else:
        cmd.execute("UPDATE login SET PASSWORD='"+newpassword+"' WHERE PASSWORD='"+oldpassword+"'")
        con.commit()
        return jsonify({'task': "Updated Succeccfully"})
    return jsonify({'task': "success"})



@flow.route("/editprofile",methods=['get','post'])
def editprofile():
    uid=request.form['uid']
    uname=request.form['uname']
    phone=request.form['phone']
    email=request.form['email']
    cmd.execute("update user_registration set usernamr='"+uname+"',phone='"+phone+"',email='"+email+"'where user_id='"+uid+"'")
    con.commit()
    return jsonify({'task':'succcess'})
# need to check
@flow.route("/traffic_control",methods=['get','post'])
def traffic_control():
    print(request.form)
    Time = request.form.get("time")
    Date = request.form.get("date")
    Location = request.form.get("location")
    route = request.form.get("route")
    loginid = request.form.get("loginid")
    cmd.execute("INSERT INTO traffic_control VALUES(NULL,'"+Time+"','"+Date+"','"+Location+"','"+route+"','"+str(loginid)+"')")
    con.commit()
    return jsonify({'task': "success"})

# @flow.route("/control_view",methods=['get','post'])
# # def control_view():
# #     cmd.execute("select * from traffic_control")
# #     s = cmd.fetchall()
# #     header = [x[0] for x in cmd.description]
# #     json_data = []
# #     for result in s:
# #         json_data.append(dict(zip(header, result)))
# #         print(json_data)
# #     return jsonify(json_data)
@flow.route("/livestats", methods=['get','post'])
def livestats():
    cmd.execute("SELECT * FROM congestion")
    s = cmd.fetchall()
    header = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        # Convert timedelta object to string representation
        result = list(result)
        result[1] = str(result[1])
        json_data.append(dict(zip(header, result)))
        print(json_data)
    return jsonify(json_data)



@flow.route("/control_view", methods=['get', 'post'])
def control_view():
    cmd.execute("SELECT * FROM traffic_control")
    s = cmd.fetchall()
    header = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        # Convert timedelta object to string representation
        result = list(result)
        result[1] = str(result[1])
        json_data.append(dict(zip(header, result)))
        print(json_data)
    return jsonify(json_data)

@flow.route("/view_all_alerts",methods=['get','post'])
def view_all_alerts():
    cmd.execute("select * from alerts")
    s = cmd.fetchall()
    header = [x[0] for x in cmd.description]
    json_data = []
    for result in s:
        json_data.append(dict(zip(header, result)))
        print(json_data)
    return jsonify(json_data)



# @flow.route('/test', methods=['GET', 'POST'])
# def test():
#     global flag_c
#     global ress
#     global res
#     try:
#         val = request.get_data().decode('utf-8')
#         print(val)
#         v=val.split(",")
#         result = "none"
#         if v[0] == "T" and flag_c == 0:
#             if ress=="none":
#                 ress="0"
#             if ress!="none":
#                 rrr=int(ress)
#                 print("a :",rrr)
#                 if rrr<=5:
#                     t_status="LOW"
#                 elif 5<rrr<=20:
#                     t_status = "MODERATE"
#                 elif rrr>20:
#                     t_status = "HIGH"
#             cmd.execute("UPDATE signal SET count='"+ress+"' , time=curtime() , status='"+str(t_status)+"' WHERE junction='"+v[1]+"'" )
#             con.commit()
#             return ress
#
#         if res == "A" or res == "B" or res == "C" or res == "D":
#             result = res
#             res = "none"
#             flag_c = 0
#             return result
#         else:
#             ress="none"
#             return ress
#     except Exception as e:
#         print(e)
#         return "error"
#
# @flow.route('/control', methods=['POST'])
# def control():
#     global res
#     global flag_c
#     try:
#         data = request.form['data']
#         print(data)
#         res = data
#         if res:
#             flag_c = 1
#         return jsonify({'result': "success"})
#
#     except Exception as er:
#         print(er)
#         return jsonify({'result': "failed"})
#
# def main():
#     threading.Thread(target=check).start()
#
# def check():
#     global ress
#     cap = cv2.VideoCapture(0)
#
#     while True:
#         _, frame = cap.read()
#         height, width, channels = frame.shape
#
#         # Detecting objects
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         net.setInput(blob)
#         outs = net.forward(output_layers)
#
#         # Showing information on the screen
#         class_ids = []
#         confidences = []
#         boxes = []
#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5:
#                     # Object detected
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#
#                     # Rectangle coordinates
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#
#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)
#
#         indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#
#         font = cv2.FONT_HERSHEY_PLAIN
#         vehicle_count = 0
#         for i in range(len(boxes)):
#             if i in indexes:
#                 x, y, w, h = boxes[i]
#                 label = str(classes[class_ids[i]])
#                 if class_ids[i] in vehicle_class_ids:
#                     vehicle_count += 1
#                     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                     cv2.putText(frame, label, (x, y + 30), font, 3, (0, 255, 0), 3)
#
#         if vehicle_count > 0:
#             # Print number of vehicles
#             print("Number of vehicles:", vehicle_count)
#             ress =str(vehicle_count)
#
#         # Display the resulting frame
#         cv2.imshow('Frame', frame)
#
#         # Exit when 'q' is pressed.
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     cap.release()
#     cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
    #main()
flow.run(host='0.0.0.0',port=5000)
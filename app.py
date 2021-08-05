import json
import os

from flask import Flask
from flask import request
from dbconnect import connectdb
from flask_cors import *



basedir = os.path.abspath(os.path.dirname(__file__))
#提取图片并存贮在固定路径
def save_image(img):
    path = basedir + "/static/img/"
    imgName = img.filename
    # 图片path和名称组成图片的保存路径
    file_path = path + imgName
    # 保存图片
    img.save(file_path)
    url = '/static/img/'+imgName
    return url
#拿到数据并且将数据插入数据库
app = Flask(__name__)
CORS(app, supports_credentials=True)
@app.route("/robotmessage", methods=["POST"])
def add_robotmessage():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    robotid = get_data.get('robotid')
    robotmessage = get_data.get('robotmap')
    # 减速度阈值
    d_threshold = get_data.get('d_threshold')
    # 定位差异阈值
    p_threshold = get_data.get('p_threshold')
    con.cursor.execute(f'''insert into robot (robotid,robotmessage,d_threshold,p_threshold) VALUES ("{robotid}","{robotmessage}","{d_threshold}","{p_threshold}")''')
    return_dict['result'] = "success"
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
@app.route("/mapmessage", methods=["POST"])
def add_mapmessage():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    robotid = get_data.get('robotid')
    creatime = get_data.get('creatime')
    mapname =get_data.get('mapname')
    map=request.files.get('map')
    map_url = save_image(map)
    con.cursor.execute(f'''insert into map (robotid,createtime,mapname,mapadress) VALUES ("{robotid}","{creatime}","{mapname}","{map_url}")''')
    return_dict['result'] = "success"
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
@app.route("/taskmessage", methods=["POST"])
def add_taskmessage():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    robotid = get_data.get('robotid')
    endtime = get_data.get('endtime')
    begintime = get_data.get('begintime')
    startplace=get_data.get('startplace')
    endplace=get_data.get('endplace')
    in_sql=f'''insert into task (robotid,begintime,startplace,endplace) VALUES ("{robotid}","{begintime}","{startplace}","{endplace}")'''
    s_sql=f'''select taskid from task where robotid="{robotid}" and begintime ="{begintime}"'''
    con.cursor.execute(in_sql)
    con.cursor.execute(s_sql)
    results=con.cursor.fetchall()
    print(results)
    return_dict['result'] = results
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
@app.route("/pointmessage", methods=["POST"])
def add_pointmessage():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    pointname = get_data.get('pointname')
    point_coordinate = get_data.get('point_coordinate')
    point_direction = get_data.get('point_direction')
    con.cursor.execute(f'''insert into point (pointname,point_coordinate,point_direction) VALUES ("{pointname}","{point_coordinate}","{point_direction}")''')
    return_dict['result'] = "success"
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
@app.route("/slammessage", methods=["POST"])
def add_slammessage():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.get_data()) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    # robotid = get_data.get('robotid')
    taskid = get_data.get('taskid')
    distance = get_data.get('distance')
    type = get_data.get('type')
    time = get_data.get('time')
    mapname=get_data.get('mapname')
    deceleration=get_data.get('deceleration')   #减速度
    coordinate=get_data.get('coordinate') #坐标
    con.cursor.execute(f'''insert into slam (taskid,distance,time,type,mapname,deceleration,coordinate) VALUES ({taskid},"{distance}","{time}","{type}","{mapname}","{deceleration}",'{coordinate}')''')
    return_dict['result'] = "success"
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
#根据机器编号和任务时间查询总任务
@app.route("/get_task", methods=["GET"])
def get_task():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.args) == 0:
        return_dict["return_code"] = "5004"
        return_dict["return_info"] = "请求参数为空"
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.args
    robotid = get_data.get('robotid')
    time = get_data.get('time')
    sql_result = con.cursor.execute(f'''select taskid,robotid,date_format(endtime, '%Y-%m-%d %H:%i:%S')  endtime,date_format(begintime, '%Y-%m-%d %H:%i:%s') begintime,startplace,endplace from task where robotid={robotid} and DATE(begintime)="{time}" ''')
    result = json.dumps(con.cursor.fetchall())
    data=f'"robotid":"{robotid}","time":"{time}","taskcount":{sql_result},"data":{result}'
    return_dict["result"] = "{%s}"%(data)
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
@app.route("/get_map", methods=["GET"])
def get_map():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.args) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    robotid = get_data.get('robotid')
    mapname = get_data.get('mapname')
    sql_result = con.cursor.execute(f'''select mapid,mapadress,mapname,date_format(createtime, '%Y-%m-%d %H:%i:%s') createtime from map where robotid="{robotid}" and mapname="{mapname}" ''')
    results = con.cursor.fetchall()
    return_dict['result'] = results[0]
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)
@app.route("/get_slam", methods=["GET"])
def get_slam():
    con = connectdb()
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': None}
    if len(request.args) == 0:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    get_data = request.values
    taskid = get_data.get('taskid')
    # starttime=get_data.get('starttime')
    # endtime=get_data.get('endtime')
    type=get_data.get('type')
    sql_result = con.cursor.execute(f'''SELECT slamid,type,mapname,deceleration,coordinate,date_format(time, '%Y-%m-%d %H:%i:%s') time from slam where type="{type}" AND taskid="{taskid}" ''')
    # AND time BETWEEN "{starttime}" AND "{endtime}"
    results = con.cursor.fetchall()
    # data=f'"count":{sql_result},"data":{results}'
    return_dict['result'] = results
    con.close()
    return json.dumps(return_dict, ensure_ascii=False)





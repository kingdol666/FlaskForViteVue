import base64
import os

from flask import Blueprint, jsonify, Flask, request, url_for, redirect, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import base64
from io import BytesIO

from machineL.ModelDemo.shici import ShiCiGet

shici = ShiCiGet()
app = Flask(__name__)
bp = Blueprint('My_Blueprint', __name__)

HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "hh20020521"
DATABASE = "flasksql1"

app.config[
    'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
app.secret_key = 'dev'
db = SQLAlchemy(app)


class Testflask(db.Model):  # 创建model，对应数据库中的表
    Id_P = db.Column(db.Integer, primary_key=True)
    LastName = db.Column(db.String(255))
    FirstName = db.Column(db.String(255))
    Address = db.Column(db.String(255))
    City = db.Column(db.String(255))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


@bp.route('/example')
def example():
    return jsonify('message', 'test!')


@app.route('/test/list', methods=['GET'])
def get_data():
    myData = Testflask.query.all()
    output = []
    for record in myData:
        r_data = {'Id_P': record.Id_P, 'FirstName': record.FirstName, 'LastName': record.LastName,
                  'Address': record.Address, 'City': record.City}
        output.append(r_data)
    return jsonify({'message': output})


@app.route('/user/list', methods=['GET'])
def get_user():
    myData = User.query.all()
    output = []
    for record in myData:
        r_data = {'Id': record.id, 'UserName': record.username, 'Email': record.email}
        output.append(r_data)
    return jsonify({'message': output})


@app.route('/user/save', methods=['POST'])
def save_user():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        username = request.form.get('username')  # 传入表单对应输入字段的 name 值
        email = request.form.get('email')
        # 验证数据
        if not username or not email or len(username) > 60 or len(email) > 60:
            print(username, email)
            flash('Invalid input.')  # 显示错误提示
            return jsonify("error: 不合法的输入")  # 重定向回主页
        # 保存表单数据到数据库
        user = User(username=username, email=email)  # 创建记录
        db.session.add(user)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        # return redirect(url_for('index'))  # 重定向回主页
    myData = User.query.all()
    output = []
    for record in myData:
        r_data = {'Id': record.id, 'UserName': record.username, 'Email': record.email}
        output.append(r_data)
    return jsonify("users:", output)


@app.route('/test/list', methods=['GET'])
def index():
    output = "hello world!"
    return jsonify({'message': output})


@app.route('/image')
def get_image():
    # Read the image file and convert it to a suitable format (e.g., Base64)
    with open('images/17.jpg', 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Return the image data as a JSON response
    return {'image': encoded_image}


@app.route('/get_image_data', methods=['GET'])
def get_image_data():
    # Read the image file
    image = Image.open('./images/2.png')

    # Convert image data to Base64 format
    image_data = base64.b64encode(image.tobytes()).decode('utf-8')

    # Return the Base64-encoded image data as a response
    return jsonify({'image_data': image_data})


# 定义路由
@app.route("/upload", methods=['POST'])
def get_frame():
    # file = request.files['file']
    # print(file.name)  # 传入表单对应输入字段的 name 值
    # return jsonify(file.name)
    # 接收图片
    upload_file = request.files['file']
    # 获取图片名
    file_name = upload_file.filename
    # 文件保存目录（桌面）
    file_path = r'./images/'
    if upload_file:
        # 地址拼接
        file_paths = os.path.join(file_path, file_name)
        # 保存接收的图片到桌面
        upload_file.save(file_paths)
        # 随便打开一张其他图片作为结果返回，
    return "ok"


@app.route("/get_blob", methods=['GET'])
def get_blob_file():
    image_dir = "./images/"
    images = []
    res = []
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Create the full path to the image
            image_path = os.path.join(image_dir, filename)
            # Add the image path to the list
            images.append(image_path)

    for img in images:
        print(img)

    for img in images:
        list_size = len(images)
        print(list_size)
        # Read the image file
        image = Image.open(img)
        # Create a binary stream
        stream = BytesIO()

        # Write the image data to the stream
        file_extension = os.path.splitext(img)[1].lower()
        if file_extension == '.jpg' or file_extension == '.jpeg':
            image.save(stream, format='JPEG')
            stream.seek(0)  # Reset the stream position
            # Return the image file as a response
            a = send_file(stream, mimetype='image/jpeg')
            res.append(a)
            return res[0]
        elif file_extension == '.png':
            image.save(stream, format='PNG')
            stream.seek(0)  # Reset the stream position
            # Return the image file as a response
            a = send_file(stream, mimetype='image/png')
            res.append(a)
            return res[0]
        else:
            # Handle unsupported file formats or other conditions
            pass
        stream.flush()
        stream.truncate(0)

    # Handle the case if no image files were found
    return res[0]


@app.route("/get_file_list", methods=['GET'])
def get_file_list():
    image_dir = "./images/"
    images = []
    res = []
    for filename in os.listdir(image_dir):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            # Create the full path to the image
            image_path = os.path.join(image_dir, filename)
            # Add the image path to the list
            images.append(image_path)

    for img in images:
        print(img)
        res.append(str(img))
    return jsonify(res)  # Return res list as JSON to the frontend


@app.route("/get_blob_byName/<path:param>", methods=['GET'])
def get_blob_by_name(param):
    if param:
        print(param)
        image = Image.open("./" + param)
        print(image)
        # Create a binary stream
        stream = BytesIO()
        file_extension = os.path.splitext(param)[1].lower()
        if file_extension == '.jpg' or file_extension == '.jpeg':
            image.save(stream, format='JPEG')
            stream.seek(0)  # Reset the stream position
            # Return the image file as a response
            a = send_file(stream, mimetype='image/jpeg')
            return a
        elif file_extension == '.png':
            image.save(stream, format='PNG')
            stream.seek(0)  # Reset the stream position
            # Return the image file as a response
            a = send_file(stream, mimetype='image/png')
            return a
        else:
            # Handle unsupported file formats or other conditions
            pass
        stream.close()
    else:
        return "No image path provided."


@app.route("/get_shici", methods=['POST'])
def get_shici():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        text = request.form.get('text')  # 传入表单对应输入字段的 name 值
        res = shici.execute(text)
        return jsonify({'text': res})
    return None


import socket
import threading
from pymysql import connect
import binascii
from redis import *
import datetime
import time
from random import randint
from celery_tasks.tcp_server.tasks import send_to_cli

# 0号库 信息交互
# 1号库 上线设备
database_host = '192.168.19.129'
server_host = '127.0.0.1'
get_msg = 3


class RedisServer(object):
    @staticmethod
    def redis_set_online(ip_key):
        try:
            # 创建StrictRedis对象，与redis服务器建⽴连接
            sr = StrictRedis(host=database_host, port=6379, db='1')
            ip_keys = ip_key[0] + ":" + str(ip_key[1])
            sr.set(ip_keys, 1)
            return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def redis_get_msg(service_client_socket, ip_key):  # last_str标记值 不允许相同
        # 第一次不发送任何消息 即使redis有信息
        # 创建StrictRedis对象，与redis服务器建⽴连接
        sr = StrictRedis(host=database_host, port=6379)
        last_str = None
        while True:
            try:
                resutl = sr.get(ip_key[0] + ":" + str(ip_key[1])).decode()  # 待改进 如果两个内容相同则不会发送给客户端
                if resutl == last_str:
                    time.sleep(3)
                else:
                    service_client_socket.send(resutl.encode(encoding='gbk'))
                    last_str = resutl
            except Exception as e:
                time.sleep(3)


class MysqlServer(object):
    @staticmethod
    def mysql_act(ip, text):
        # 创建Connection连接

        conn = connect(host=database_host, port=3306, user='root', password='mysql', database='django',
                       charset='utf8')
        # 获得Cursor对象
        cs1 = conn.cursor()

        # 安全的方式
        # 构造参数列表
        # 执行select语句，并返回受影响的行数：查询所有数据
        count = cs1.execute("insert into tb_facility values(DEFAULT,%s,%s);",
                            [ip, text])
        # 注意：
        # 如果要是有多个参数，需要进行参数化
        # 那么params = [数值1, 数值2....]，此时sql语句中有多个%s即可
        # 打印查询的结果
        conn.commit()
        # 关闭Cursor对象
        cs1.close()
        # 关闭Connection对象
        conn.close()  # 处理客户端的请求操作

    @staticmethod
    def mysql_select(ip):
        try:
            # 创建Connection连接
            conn = connect(host=database_host, port=3306, user='root', password='mysql', database='django',
                           charset='utf8')
            # 获得Cursor对象
            cs1 = conn.cursor()
            # 安全的方式
            # 构造参数列表
            # 执行select语句，并返回受影响的行数：查询所有数据
            cs1.execute("select device_name from tb_facility where device_code=%s;", ip)
            result = cs1.fetchall()
            # 打印查询的结果
            # 关闭Cursor对象
            cs1.close()
            # 关闭Connection对象
            conn.close()  # 处理客户端的请求操作
            return result
        except Exception as e:
            print('mysql数据库连接失败：%s', e)


class Hex(object):
    @staticmethod
    def str_to_hexStr(string):
        str_bin = string.encode()
        return binascii.hexlify(str_bin).decode()

    @staticmethod
    def hexStr_to_str(hex_str):
        hex = hex_str.encode()
        str_bin = binascii.unhexlify(hex)
        return str_bin.decode('utf-8')


def handle_client_request(service_client_socket, ip_port):
    # 为了让发送创建线程只执行一次
    bool_str = True
    # 设备上线
    RedisServer.redis_set_online(ip_port)
    # 循环接收客户端发送的数据
    while True:
        # 接收客户端发送的数据
        recv_data = service_client_socket.recv(1024).decode(encoding='gbk')
        if recv_data:
            print(recv_data, ip_port)
            # MysqlServer.mysql_act(ip_port[0], recv_data)      # 不从这里加ip到mysql 在web注册才可以
            if bool_str:
                # 发送消息另开线程处理
                send_msg_thread = threading.Thread(target=RedisServer.redis_get_msg,
                                                   args=(service_client_socket, ip_port))
                send_msg_thread.setDaemon(True)
                send_msg_thread.start()
                now_time = datetime.datetime.now()
                print(f'已发送 时间戳{now_time}')
                bool_str = False


        else:
            sr = StrictRedis(host=database_host, port=6379, db=1)
            ip_keys = ip_port[0] + ":" + str(ip_port[1])
            sr.delete(ip_keys)
            print("客户端下线了:", ip_port)
            break
    # 终止和客户端进行通信
    service_client_socket.close()


if __name__ == '__main__':

    # 创建tcp服务端套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口号复用，让程序退出端口号立即释放
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口号
    tcp_server_socket.bind((server_host, 9000))
    # 设置监听, listen后的套接字是被动套接字，只负责接收客户端的连接请求
    tcp_server_socket.listen(128)
    # 循环等待接收客户端的连接请求
    while True:
        # 等待接收客户端的连接请求
        service_client_socket, ip_port = tcp_server_socket.accept()
        if MysqlServer.mysql_select(ip_port[0]):
            print("客户端连接成功:", ip_port)
            # 当客户端和服务端建立连接成功以后，需要创建一个子线程，不同子线程负责接收不同客户端的消息
            sub_thread = threading.Thread(target=handle_client_request, args=(service_client_socket, ip_port))
            # 设置守护主线程
            sub_thread.setDaemon(True)
            # 启动子线程
            sub_thread.start()
        else:
            data = "设备未注册，拒绝连接"  # 后续记录到日志里面
            service_client_socket.send(data.encode(encoding='gbk'))
            service_client_socket.close()
            # tcp服务端套接字可以不需要关闭，因为服务端程序需要一直运行
            # tcp_server_socket.close()

from celery_tasks.celery import app

@app.task(bind=True)
def send_to_cli(param, service_client_socket):
    print(service_client_socket)
    # 从django获取msg
    data = input(msg)
    service_client_socket.send(data.encode(encoding='gbk'))
    return True

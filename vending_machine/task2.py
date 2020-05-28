import jwt
# _payload = {'exp': 3600*2*24}
# _payload.update({"das":"22"})
token = jwt.encode({"das":"22"}, "dasd", algorithm='HS256', )
print(token)
payload = jwt.decode(token, "dasd", algorithm=['HS256'])
print(payload)
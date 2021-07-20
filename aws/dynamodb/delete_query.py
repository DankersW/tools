import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('vayyar_home_c2c_room_status')

# DB structure
# {'device_id', 'timestamp', 'room_occupied}
device_id = 'id_MzA6QUU6QTQ6RTQ6MDA6NTQ'

# Scan the entire table
#scan_data = table.scan()
#print(scan_data)

# Query data
timestamp = 1626771354887
query = Key('device_id').eq(device_id) & Key('timestamp').gte(timestamp)
#query_data = table.query(KeyConditionExpression=query)
#print(query_data)

print("oke")

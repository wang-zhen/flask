#users
curl -i 172.16.103.18:5000/v1/storage/users
curl -i -X POST -H "Content-Type:application/json" -d '{"username":"wangzhen"}' 172.16.103.18:5000/v1/storage/users
curl -i 172.16.103.18:5000/v1/storage/users/1
curl -i -X DELETE 172.16.103.18:5000/v1/storage/users/1

#subusers
curl -i 172.16.103.18:5000/v1/storage/subusers
curl -i -X POST -H "Content-Type:application/json" -d '{"user_id":1, "username":"wangzhen"}' 172.16.103.18:5000/v1/storage/subusers
curl -i 172.16.103.18:5000/v1/storage/subusers/1
curl -i -X DELETE 172.16.103.18:5000/v1/storage/subusers/1

#subusers
curl -i 172.16.103.18:5000/v1/storage/userkeys
curl -i -X POST -H "Content-Type:application/json" -d '{"user_id":1}' 172.16.103.18:5000/v1/storage/userkeys
curl -i 172.16.103.18:5000/v1/storage/userkeys/2
curl -i -X DELETE 172.16.103.18:5000/v1/storage/userkeys/2

#buckets
curl -i 172.16.103.18:5000/v1/storage/bucket
curl -i -X POST -H "Content-Type:application/json" -d '{"user_id":1}' 172.16.103.18:5000/v1/storage/userkeys
curl -i 172.16.103.18:5000/v1/storage/userkeys/2
curl -i -X DELETE 172.16.103.18:5000/v1/storage/userkeys/2

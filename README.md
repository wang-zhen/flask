1. Flask tree
.
├── apps1
│   ├── control.py
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── apps2
│   ├── control.py
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── agent
│   ├── celery.py
│   ├── cephrgw_buckets.py
│   ├── cephrgw_objects.py
│   ├── cephrgw_users.py
│   ├── common.py
│   ├── comm_path.py
│   └── __init__.py
├── buckets
│   ├── control.py
│   ├── __init__.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── common
│   ├── db.py
│   ├── fclog.py
│   ├── __init__.py
│   ├── serializer.py
│   └── status.py
├── manager.py
├── README.md
├── requirements.txt

2.db operations
#python manager.py  db init
#python manager.py  db migrate
#python manager.py  db upgrade

3.how to work
 #./src/redis-server *:6379 
 # cd fusioncloud
 # celery worker -A agent --loglevel=info
 # python manager.py  runserver 



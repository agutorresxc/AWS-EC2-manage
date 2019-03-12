#!/usr/bin/python
import time
import sys
import boto3


key='your key'
skey='your secret key'
region = 'us-east-1'
sleepdelta = 15

def _help():
    print ("""
Uso:
    python ec2Gestar.py <command> [lista de instancias]

Commands:
    start
    stop
    list
    help
    
Ejemplo: Iniciar una instancia

    python ec2Gestar.py start i-xxxxxxxxxxx

Ejemplo 2: Iniciar varias instancias

    python ec2Gestar.py start i-xxxxxxxxxxx i-zzzzzzzzzz

Ejemplo 3: Apagar instancia

    python ec2Gestar.py stop i-xxxxxxxxxxx

    
Ejemplo 4: Listar datos de instancias

    python ec2Gestar.py list 

           """)

def _printInstances():
    resource = boto3.resource('ec2', region_name=region, aws_access_key_id=key, aws_secret_access_key=skey)
    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    for i in resource.instances.filter(Filters=filters):
        name = [x.get('Value') for x in i.tags if x['Key'] == 'Name'][0]
        print ("ID: %s\t Nombre: %s\t IP Publica: %s\tIP Privada: %s)" % (i.id, name, str(i.public_ip_address or ""), i.private_ip_address ))

def start(instances):
    
    client = boto3.client('ec2', region_name=region, aws_access_key_id=key, aws_secret_access_key=skey)
    
    client.start_instances(InstanceIds=instances)

    #for i in range (sleepdelta):
    #    print ("procesando %s" % (str("." *i)))
    #    time.sleep( 1 )

    #print ("\n\n")
    
    #_printInstances()

def stop(instances):
    
    client = boto3.client('ec2', region_name=region, aws_access_key_id=key, aws_secret_access_key=skey)
    client.stop_instances(InstanceIds=instances)


_instances = sys.argv[1:]

if len(_instances) == 0:
    _help()
    exit(0)

command = _instances[0]

_instances = _instances[1:]

if command == 'start':
    start(_instances)
elif command == 'stop':
    stop(_instances)
elif command == 'list':
    _printInstances()
else:
    _help()


    

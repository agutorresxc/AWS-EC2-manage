# AWS-EC2-manage


![#c5f015](https://placehold.it/15/c5f015/000000?text=+) `Español`

# Administrar Instancias AWS - EC2

> Las instancias EC2 en amazon son maquinas virtuales, windows o linux que se incluyen dentro de una red virtual en la nube. Esta red virtual se la conoce como VPC (virtual private cloud)

## Consumo
Uno de los problemas más comunes con los recursos cloud, son el consumo, o mejor dicho, la cantidad de tiempo que están disponibles on line. Cuando tenemos un recurso productivo, queremos que este este 100% funcionando. ¿Pero que ocurre con los recursos de test o desarrollo? que deben estar vivos en horarios determinados? Para esto requerimos apagar y prender los equipos en momentos determinados. 

## Apagado
Para comenzar, veremos como apagar los equipos.
Para esto, solo necesitamos

```python
#import boto3 library
import boto3
# choice region
region = 'us-east-1'
#create object
ec2 = boto3.client('ec2', region_name=region)
#stop instance
ec2.stop_instances(InstanceIds='i-xxxxxxxx')
```
> el ejemplo anterior, sirve para apagar una sola instancia.

Veamos ahora un ejemplo completo, donde se toman las instancias según tag's de las instancias EC2 para saber si hay que apagarlas o no.

```python
import boto3
from botocore.exceptions import ClientError

region = 'us-east-1'

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    
    instances = []
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append (instance["InstanceId"])
    
    stop_instances = []
    tabla =  "<table><tr><td>Nombre</td><td>Instancia ID</td></tr>"
    ec2r = boto3.resource('ec2')
    
    for instance in instances:
        i = ec2r.Instance(id=instance)
        ambiente = False
        apagado = False
        tipo = False
        name = ""
        
        for tag in i.tags:
            if tag['Key'] == "Ambiente" and (tag.get('Value') == "Desarrollo" or tag.get('Value') == "Test") :
                ambiente = True
            
            if tag['Key'] == "Tipo" and tag.get('Value') == "Gestar":
                tipo = True
                
            if tag['Key'] == "apagadoNocturno" and tag.get("Value") == "Si":
                apagado = True
                
            if tag['Key'] == 'Name':
                name = tag.get('Value')
            
        if ambiente and apagado and tipo:
            stop_instances.append(instance)
            tabla += "<tr><td>" + name + "</td><td>" + instance + "</td><td>"
            
    tabla +="</table>"
    
    #si = ",".join([x for x in stop_instances])
    ec2.stop_instances(InstanceIds=stop_instances)
    
    SENDER = "Afonso Palomares <apalomares@xxxx.com>"
    RECIPIENT = "soporte@xxxx.com"
    AWS_REGION = region
    SUBJECT = "ENVIO AMAZON -- >> STOP instances"
    CHARSET = "UTF-8"
    BODY_TEXT = ("Apagando EC2 instances...\r\n"
                 "Este mail es enviado automaticamente por AWS SES al ejecutar "
                 "la funcion lambda de AWS SDK"
                )
    BODY_HTML = "<html> <head></head> <body> <h1>Apagando EC2 Instancias...</h1>"
    BODY_HTML += tabla          
    #BODY_HTML += "<br/>" + si
    BODY_HTML += "</body></html>"
    
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])
    
```
> El codigo anterior, no solo apaga las EC2 en base a los tags ambiente, apagadoNocturno y tipo, sino que luego, envía un correo notificando.

## Encendido
El encendido es muy similar al apagado, solo cambia la instrucción requerida

```python
#import boto3 library
import boto3
# choice region
region = 'us-east-1'
#create object
ec2 = boto3.client('ec2', region_name=region)
#stop instance
ec2.start_instances(InstanceIds='i-xxxxxxxx')
```
> el ejemplo anterior, sirve para prender una sola instancia.

Ahora, veamos un ejemplo completo, que enciende todas las instancias que cumplan con los TAG's requeridos

```python

import boto3
from botocore.exceptions import ClientError

# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'us-east-1'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    
    instances = []
    response = ec2.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instances.append (instance["InstanceId"])
    
    
    #print instances 
    start_instances = []
    tabla =  "<table><tr><td>Nombre</td><td>Instancia ID</td></tr>"
    ec2r = boto3.resource('ec2')
    
    for instance in instances:
        i = ec2r.Instance(id=instance)
        ambiente = False
        encendido = False
        tipo = False
        name = ""
        
        for tag in i.tags:
            if tag['Key'] == "Ambiente" and (tag.get('Value') == "Desarrollo" or tag.get('Value') == "Test") :
                ambiente = True
            
            if tag['Key'] == "Tipo" and tag.get('Value') == "Gestar":
                tipo = True
                
            if tag['Key'] == "encendidoDiurno" and tag.get("Value") == "Si":
                encendido = True
            
            if tag['Key'] == 'Name':
                name = tag.get('Value')        
                
        if ambiente and encendido and tipo:
            start_instances.append(instance)
            tabla += "<tr><td>" + name + "</td><td>" + instance + "</td><td>"
            
    tabla +="</table>"        
    
    #si = ",".join([x for x in start_instances])
    ec2.start_instances(InstanceIds=start_instances)
    
    SENDER = "Afonso Palomares <apalomares@gestar.com>"
    RECIPIENT = "soporte@gestar.com"
    AWS_REGION = region
    SUBJECT = "ENVIO AMAZON -- >> START instances"
    CHARSET = "UTF-8"
    BODY_TEXT = ("Prendiendo EC2 instances...\r\n"
                 "Este mail es enviado automaticamente por AWS SES al ejecutar "
                 "la funcion lambda de AWS SDK."
                )
    BODY_HTML = "<html> <head></head> <body> <h1>Prendiendo EC2 Instancias...</h1>"
    BODY_HTML += tabla          
    #BODY_HTML += "<br/>" + si
    BODY_HTML += "</body></html>"
    
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['ResponseMetadata']['RequestId'])
    
```

![#1589F0](https://placehold.it/15/1589F0/000000?text=+) `English`

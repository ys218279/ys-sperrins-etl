import boto3
import json


# This is the entry function which will only be used once to create the initial secret that will store the totesys DB credentials
def entry(client):
    """Create a new secret called de_2024_12_02 in aws secrets manager.
    
    Required input argument: 
    - client (aws secrets manager client)
    
    Exceptions raised:
    - ResourceExistsException i.e. Secret already exists.
    """
    if "SecretsManager" in str(type(client)):
        secret_identifier = "de_2024_12_02"
        get_username = input('Please enter your username:')
        get_password = input("Please enter your password:")
        get_host = input("Please enter your host:")
        get_database = input("Please enter your database:")
        get_port = input("Please enter your port:")
        secret_value = {"username": get_username,
                        "password": get_password,
                        "host": get_host,
                        "database": get_database,
                        "port": get_port}
        secret_string = json.dumps(secret_value)
        try:
            client.create_secret(Name=secret_identifier, SecretString=secret_string)
            print("Secret saved.")
        except client.exceptions.ResourceExistsException as e:
            print("Secret already exists!")
        except Exception as err:
            print({"ERROR": err, "message": "Fail to connect to aws secret manager!"})
    else:
        print("invalid client type used for secret manager! plz contact developer!")

#This is the retrieval function which accesses the secret storing the totesys DB credentials as a dictionary
#This function can be used multiple times whenever user needs DB credentials in lambda
def retrieval(client):
    """Retrieve a secret called de_2024_12_02 from aws secrets manager.
    
    Required input argument:
    - client (aws secrets manager client)

    Exceptions raised:
    - ResourceNotFoundException i.e. secret ID does not exist.
    """
    if "SecretsManager" in str(type(client)):
        secret_identifier = "de_2024_12_02"
        try:
            response = client.get_secret_value(SecretId=secret_identifier)
            res_str = response["SecretString"]
            res_dict = json.loads(res_str)
            print("Secrets returned as dictionary")
            return res_dict
        except client.exceptions.ResourceNotFoundException as err:
            print(err)
        except Exception as err:
            print({"ERROR": err, "massage": "Fail to connect to aws secret manager!"})
    else:
        print("invalid client type used for secret manager! plz contact developer!")

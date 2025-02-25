import boto3
import json

def entry(client):
    if "SecretsManager" in str(type(client)):
        secret_identifier = "de_2024_12_02"
        get_username = input('Please enter your username: ')
        get_password = input("Please enter your password:")
        get_host = input("Please enter your host: ")
        get_database = input("Please enter your database: ")
        get_port = input("Please enter your port: ")
        secret_value = {"username": get_username,
                        "password": get_password,
                        "host": get_host,
                        "database": get_database,
                        "get_port": get_port}
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


def retrieval(client):
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



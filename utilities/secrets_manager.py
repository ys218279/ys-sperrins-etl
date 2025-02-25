import boto3
import maskpass
import json



def entry(client):
    if "SecretsManager" in str(type(client)):
        secret_identifier = "de_2024_12_02"
        get_username = input('Please enter your username: ')
        get_password = maskpass.askpass(prompt="Please enter your password: ", mask="#")
        get_host = maskpass.askpass(prompt="Please enter your host: ", mask="#")
        get_database = maskpass.askpass(prompt="Please enter your database: ", mask="#")
        get_port = maskpass.askpass(prompt="Please enter your port: ", mask="#")
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
        
client = boto3.client('secretsmanager')

def password_retrieval(client):
    id_input = input('Specify secret to retrieve:')
    try:
        response = client.get_secret_value(
        SecretId=id_input)
        sec_str = response['SecretString']
        comma_index = sec_str.rfind(',')
        user_str = sec_str[1:comma_index] + '\n'
        pass_str = sec_str[comma_index+1:len(sec_str)-1]
        file = open("secrets.txt", "w")
        file.writelines([user_str, pass_str])
        file.close()
        return (f'secrets stored in {file.name}')
    
    except client.exceptions.ResourceNotFoundException as e:
        return 'Secret not found'




{"cohort_id": "de_2024_12_02",
"user": "project_team_9",
"password": "a16AUVpWb8lZ6rV",
"host": "nc-data-eng-totesys-production.chpsczt8h1nu.eu-west-2.rds.amazonaws.com",
"database": "totesys",
"port": 5432}


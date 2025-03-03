import json


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

import boto3, json
from botocore.exceptions import ClientError

def load_retrieval(client, secret_identifier="totesys_data_warehouse_olap"):
    """Return the credentials to the final Data Warehouse as a dictionary.
    
    Required input arguments:
    - client = secrets manager client
    - secret identifier (default = "totesys_data_warehouse_olap")

    Returns:
    - credentials required for connecting to db as dictionary containing key:value pairs

    Errors logged and raised:
    - Resource Not Found
    - Client Errors from AWS side.
    """  
    try:
        response = client.get_secret_value(SecretId=secret_identifier)
        res_str = response["SecretString"]
        res_dict = json.loads(res_str)
        return res_dict
    except client.exceptions.ResourceNotFoundException as err:
        print(err)
        # call sns publish here.
    except ClientError as err:
        print({"ERROR": err, "message": "AWS Error detected and logged!"})
        # call sns publish here.
    
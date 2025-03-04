import boto3
from botocore.exceptions import ClientError
import json
from datetime import datetime
from pg8000.native import Connection
import sys

sys.path.append("src/src_ingestion")


def entry(client):
    """will only be used once to create the initial secret that will store the totesys DB credentials"""
    if "SecretsManager" in str(type(client)):
        secret_identifier = "de_2024_12_02"
        get_username = input("Please enter your username: ")
        get_password = input("Please enter your password:")
        get_host = input("Please enter your host: ")
        get_database = input("Please enter your database: ")
        get_port = input("Please enter your port: ")
        secret_value = {
            "username": get_username,
            "password": get_password,
            "host": get_host,
            "database": get_database,
            "port": get_port,
        }
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

def retrieval(client, secret_identifier="de_2024_12_02"):
    """return the credentials to the totesys db in a dictionary"""
    if "SecretsManager" in str(type(client)):
        try:
            response = client.get_secret_value(SecretId=secret_identifier)
            res_str = response["SecretString"]
            res_dict = json.loads(res_str)
            return res_dict
        except client.exceptions.ResourceNotFoundException as err:
            print(err)
        except Exception as err:
            print({"ERROR": err, "massage": "Fail to connect to aws secret manager!"})
    else:
        print("invalid client type used for secret manager! plz contact developer!")


def connect_to_db(secret_identifier="de_2024_12_02"):
    """return conn to totesys db"""
    client = get_secrets_manager_client()
    credentials = retrieval(client, secret_identifier=secret_identifier)

    if not credentials:
        entry(client)
        credentials = retrieval(client)

    return Connection(
        user=credentials["username"],
        password=credentials["password"],
        database=credentials["dbname"],
        host=credentials["host"],
    )


def close_db_connection(conn):
    """close db"""
    conn.close()


def get_s3_client():
    """return a client to connect to s3"""
    try:
        client = boto3.client("s3", region_name="eu-west-2")
        return client
    except ClientError:
        raise ClientError(
            {
                "Error": {
                    "Code": "FailedToConnect",
                    "Message": "failed to connect to s3",
                }
            },
            "GetS3Client",
        )


def get_secrets_manager_client():
    """return a client to connect to secret manager"""
    try:
        client = boto3.client("secretsmanager", region_name="eu-west-2")
        return client
    except ClientError:
        raise ClientError(
            {
                "Error": {
                    "Code": "FailedToConnect",
                    "Message": "failed to connect to secret manager",
                }
            },
            "GetSecretsManagerClient",
        )


def upload_to_s3(bucket_name, table, result):
    """upload the file to s3 bucker and return the object name"""
    tmp_file_path = f"/tmp/{table}.json"
    with open(tmp_file_path, "w") as f:
        filedatain = json.dumps(result, indent=4, sort_keys=True, default=str)
        res_bytes = filedatain.encode("utf-8")
    s3_client = get_s3_client()
    y_m_d = datetime.now().strftime("%Y%m%d")
    filename = datetime.now().strftime("%H%M%S")
    object_name = f"{table}/{y_m_d}{filename}"
    s3_client.put_object(Body=res_bytes, Bucket=bucket_name, Key=object_name)
    return object_name

def fetch_latest_update_time_from_s3(client, bucket_name, table_name):
    """fetch the latest time of the file being loaded to s3 bucket and return the latest upload time as int."""
    response = client.list_objects_v2(Bucket=bucket_name, Prefix=table_name + "/")
    raw_all_updates = response.get("Contents", [])
    if raw_all_updates:
        all_tables = [update["Key"].split("/")[0] for update in raw_all_updates]
        if table_name not in all_tables:
            return 20000101000001
        all_updates = [update["Key"].split("/")[-1] for update in raw_all_updates]
        last_update = max(list(map(int, all_updates)))
        return last_update
    return 20000101000001

def fetch_latest_update_time_from_db(conn, table_name):
    """fetch the latest update of the table in db and return the latest update time as int."""
    query = f"SELECT last_updated FROM {table_name} ORDER BY last_updated DESC LIMIT 1;"
    raw_last_updated = conn.run(query)
    last_updated_dt = raw_last_updated[0][0]
    formatted_res = int(last_updated_dt.strftime("%Y%m%d%H%M%S"))
    return formatted_res

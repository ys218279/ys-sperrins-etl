import boto3

# sends email containing error
def sns_publish(client,content):
    # gets topic arn
    topic_response = client.create_topic(Name='Lambda_ingestion_topic')
    topic_arn = topic_response["TopicArn"]
    # publishes error message to all subscribed emails
    response = client.publish(TopicArn=topic_arn,
                   Message=content,
                   Subject='Ingestion Lambda Excecution Failure')
    return response





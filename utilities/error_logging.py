import boto3, logging

# setup a cloudwatch alarm to trigger when a lambda fails


def cloudwatch_logs(client, logGroupName):
    # we want to watch the lambda function and logg success and failures
    log_stream_response = client.describe_log_streams(logGroupName=logGroupName)
    latest_stream_response = log_stream_response["logStreams"][-1]
    log_event_response = client.get_log_events(
        logGroupName=logGroupName, logStreamName=latest_stream_response["logStreamName"]
    )
    print(log_event_response)


def subscribe_to_sns(client, email_address):

    # 1) create topic
    topic_response = client.create_topic(Name="lambda_Ingestion_topic")
    topic_arn = topic_response["TopicArn"]
    print(topic_arn)
    # 2)subscribe to email to send responses to
    sub_response = client.subscribe(
        TopicArn=topic_arn, Protocol="email", Endpoint=email_address
    )
    print(sub_response)
    return topic_arn


def get_sub_arn(client,topic_arn,email_address):
    sub_arn_response = client.list_subscriptions_by_topic(TopicArn=topic_arn)
    #print(sub_arn_response)
    for subscription in sub_arn_response['Subscriptions']:
        if subscription['Endpoint'] == email_address:
            return subscription['SubscriptionArn']



def pubslish_thingy(client,topic_arn):
    # 3)use publish to send message to email

    # 4) make cloudwatch alarm and link to sns
    pass


session = boto3.session.Session()
log_client = session.client(service_name="logs", region_name="eu-west-2")
sns_client = session.client(service_name="sns", region_name="eu-west-2")



# cloudwatch_logs(client,'/aws/lambda/roll_dice')
#subscribe_to_sns(sns_clinet, "ys218279@gmail.com")
#topic_arn = 'arn:aws:sns:eu-west-2:626635445038:lambda_Ingestion_topic'

topic_arn = subscribe_to_sns(sns_client,"ys218279@gmail.com")
sub_arn = get_sub_arn(sns_client,topic_arn,'ys218279@gmail.com')
print(sub_arn)
confirm_subscription(sns_client,sub_arn)


#confirm_subscription(sns_clinet,topic_arn)


# lambda executes -> passed -> log the pass
#                -> fails  -> log failure -> get the response with cloudwatch func

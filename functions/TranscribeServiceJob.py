import boto3
import os
import uuid
import logging
import json

# Configure logging
#logger = logging.getLogger()
#logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Retrieve the S3 bucket and object information from the event
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']
    # Generate a unique job name and output file name
    job_name = str(uuid.uuid4())

    destination_bucket = os.environ['S3_DESTINATION_BUCKET']
    
    # Create an Amazon Transcribe client
    transcribe_client = boto3.client('transcribe')
    #
    # Set Media file URI for input audio file
    media_file_uri = f"s3://{s3_bucket}/{s3_key}"
    output_file_name = f"transcribe-output/{s3_key}-redacted.json"
    
    # Start the transcription job
    response = transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                LanguageCode='en-US',
                Media={
                    'MediaFileUri': media_file_uri
                },
                OutputBucketName=destination_bucket,
                OutputKey=output_file_name,
    
                ContentRedaction={
                    'RedactionType': 'PII',
                    'RedactionOutput': 'redacted'
                }
        )

    transcription_job = response.get('TranscriptionJob', {})
    
    result = {
        'TranscriptionJobName': transcription_job.get('TranscriptionJobName'),
        'TranscriptionJobStatus': transcription_job.get('TranscriptionJobStatus'),
        'LanguageCode': transcription_job.get('LanguageCode'),
        'MediaFileUri': transcription_job.get('Media', {}).get('MediaFileUri'),
        'OutputBucketName': destination_bucket,
        'OutputKey': output_file_name,
        'StartTime': transcription_job.get('StartTime').isoformat() if transcription_job.get('StartTime') else None,
        'CreationTime': transcription_job.get('CreationTime').isoformat() if transcription_job.get('CreationTime') else None
    }
    
    print(f"Transcription job started: {json.dumps(result)}")
    
    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
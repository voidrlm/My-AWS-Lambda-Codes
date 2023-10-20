# Add layer to the lambda function
# arn:aws:lambda:ap-south-1:770693421928:layer:Klayers-p38-Pillow:9
import json
import boto3
import logging
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
bucket_name = ''  # bucket name here


def lambda_handler(event, context):
    try:
        image_key = ''  # image key here (path of imagein s3)

        response = s3.get_object(Bucket=bucket_name, Key=image_key)
        file = response['Body'].read()
        gpsData = extractGPSDataFromImage(file)
        response = {
            'statusCode': 200,
            'body': json.dumps(gpsData)
        }
    except Exception as e:
        response = {
            'statusCode': 500,  # Indicates a server error
            'body': json.dumps('Error: ' + str(e))
        }

    return response


def extractGPSDataFromImage(image):
    try:
        img = Image.open(io.BytesIO(image))
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == 'GPSInfo':
                    gps_info = {GPSTAGS.get(t, t): v for t, v in value.items()}
                    latitude = gps_info.get('GPSLatitude')
                    longitude = gps_info.get('GPSLongitude')

                    if latitude and longitude:
                        latitude = float(
                            latitude[0]) + float(latitude[1]) / 60 + float(latitude[2]) / 3600
                        longitude = float(
                            longitude[0]) + float(longitude[1]) / 60 + float(longitude[2]) / 3600
                        if gps_info.get('GPSLatitudeRef') == 'S':
                            latitude = -latitude
                        if gps_info.get('GPSLongitudeRef') == 'W':
                            longitude = -longitude

                        return latitude, longitude
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

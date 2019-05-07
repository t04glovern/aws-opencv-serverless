import boto3
import cv2
import numpy as np
import uuid
import os

s3Client = boto3.client('s3')


def opencv(event, context):
    bucketName = event['Records'][0]['s3']['bucket']['name']
    bucketKey = event['Records'][0]['s3']['object']['key']

    download_path = '/tmp/{}{}'.format(uuid.uuid4(), bucketKey)
    output_path = '/tmp/{}'.format(bucketKey)

    s3Client.download_file(bucketName, bucketKey, download_path)

    try:
        img = cv2.imread(download_path)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
        gray = cv2.dilate(gray, kernel, iterations=1)

        ret,gray = cv2.threshold(gray, 254, 255, cv2.THRESH_TOZERO)
        ret,gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV)

        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for index in range(len(contours)):
            i = contours[index]
            area = cv2.contourArea(i)
            if area > 500:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.1*peri,True)
                if len(approx)==4:
                        hull = cv2.convexHull(contours[index])
                        cv2.imwrite(output_path, cv2.drawContours(img, [hull], 0, (0,255,0),3))
    except Exception as e:
        print(e)
        print('Error processing file with OpenCV')
        raise e
    try:
        s3Client.upload_file(output_path, os.environ['OPENCV_OUTPUT_BUCKET'], bucketKey)
    except Exception as e:
        print(e)
        print('Error uploading file to output bucket')
        raise e
    return bucketKey
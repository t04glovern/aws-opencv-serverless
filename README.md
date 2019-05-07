# OpenCV on Lambda

Run OpenCV 4.0 on Lambda using Serverless framework. Extract images from scanned documents

## Serverless Setup

```bash
## Project Setup
mkdir opencv-serverless
cd opencv-serverless
serverless create --template aws-python3 --name opencv-serverless
```

### Requirements

```bash
serverless plugin install -n serverless-python-requirements
```

Create a `requirements.txt` file with the following

```bash
opencv-python==4.1.0.25
numpy==1.16.3
```

Also add the following to the `custom` area in the serverless.yaml template.

```bash
custom:
    pythonRequirements:
        dockerizePip: non-linux
        noDeploy: []
```

### Deploy

```bash
serverless deploy
```

### Test

```bash
aws s3 cp in/square-test.png s3://devopstar-opencv-processing-bucket/square-test.png
aws s3 cp s3://devopstar-opencv-output-bucket/square-test.png out/square-test.png
```
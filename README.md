# pipeline-tracker

## Getting started
### Install prerequisites
Required: python3 and pip

`pip install -r requirements.txt`

### Run the pipeline tracker application server
`gunicorn --config gconfig.py app:app`
The application will listen at port 8000 by default

## Custom configuration

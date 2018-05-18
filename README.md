# Image_Processor
Created with [Serverless Python Template](https://github.com/FindawayWorld/cookiecutter-serverless-python)

A short description of the service

## Getting Started
To create the custom domain for this service:
```
sls create_domain
```
To deploy the service:
```
sls deploy
```
To test the deployed function:
```
curl https://image_processor-dev.findaway.com/
```
To view logs for a function:
```
sls logs -t -f get_image
```
To remove the service:
```
sls remove
sls delete_domain
```
To deploy to production:
```
sls create_domain --stage prod
sls deploy --stage prod
```

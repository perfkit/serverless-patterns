# https://hub.docker.com/r/nikolaik/python-nodejs
# CDK recommends using an active LTS version of nodejs: https://github.com/aws/aws-cdk
FROM nikolaik/python-nodejs:python3.9-nodejs16

# https://www.npmjs.com/package/aws-cdk
# or latest
ARG AWS_CDK_VERSION=1.132.0
ENV AWS_CDK_VERSION $AWS_CDK_VERSION

# Install AWS CDK globally
RUN npm install -g aws-cdk@${AWS_CDK_VERSION}

# Install Python app dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

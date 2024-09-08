FROM public.ecr.aws/lambda/python:3.12

RUN dnf update -y && dnf install -y gcc-c++
RUN dnf install -y java-11-amazon-corretto-devel

# Install Node.js for JavaScript execution
RUN dnf install -y nodejs

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]
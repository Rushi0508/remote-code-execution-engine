FROM public.ecr.aws/lambda/nodejs:20 as builder
WORKDIR /usr/app
COPY package.json index.ts  ./
RUN npm install
RUN npm run build

FROM public.ecr.aws/lambda/nodejs:20

# Install Python
RUN microdnf update && \
    microdnf install -y python3 python3-pip && \
    microdnf clean all && \
    rm -rf /var/cache/yum

# Install OpenJDK for Java
RUN microdnf install -y java-11-amazon-corretto-devel

# Install GCC for C++
RUN microdnf install -y gcc-c++ make

WORKDIR ${LAMBDA_TASK_ROOT}
COPY --from=builder /usr/app/dist/* ./
CMD ["index.handler"]
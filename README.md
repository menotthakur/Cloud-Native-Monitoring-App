# **Cloud Native Resource Monitoring Python App on Kubernetes**

## **Project Overview** 
This project demonstrates how to build a **Cloud-Native Resource Monitoring Application** using **Python, Flask, and Kubernetes**. The app provides real-time system metrics using the `psutil` library and is deployed on **Amazon EKS (Elastic Kubernetes Service)**.



1. **Python**: Developing a Monitoring Application using Flask and `psutil`.
2. **Running a Python App Locally**.
3. **Docker**: Containerizing the Python app.
    - Writing a `Dockerfile`
    - Building Docker Images
    - Running Docker Containers
    - Useful Docker Commands
4. **Amazon ECR**: Creating an Elastic Container Registry (ECR) and pushing Docker images using Python's **Boto3**.
5. **Kubernetes**: Deploying the app on **Amazon EKS**.
6. **Automating Kubernetes Deployments and Services** using Python.

## **Prerequisites** 

Before starting, make sure you have:

- [x] An **AWS Account**
- [x] **Programmatic Access** configured with the AWS CLI
- [x] **Python 3** installed
- [x] **Docker & Kubectl** installed
- [x] A **Code Editor** (VS Code preferred)

---

# **Project Implementation**

## **Part 1: Running the Flask App Locally**

### **Step 1: Install Dependencies**

The application requires the following Python libraries: `psutil`, `Flask`, `Plotly`, and `Boto3`. Install them using:

```bash
pip3 install -r requirements.txt
```

### **Step 2: Run the Flask App**

Navigate to the project root directory and execute:

```bash
python3 app.py
```

This starts the Flask server on **`localhost:5000`**. Open your browser and visit **[http://localhost:5000/](http://localhost:5000/)**.

---

## **Part 2: Dockerizing the Flask Application**

### **Step 1: Create a Dockerfile**

Create a `Dockerfile` in the project root with the following contents:

```Dockerfile
# Use an official Python image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set Flask environment variables
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the application port
EXPOSE 5000

# Start the Flask app
CMD ["flask", "run"]
```

### **Step 2: Build the Docker Image**

```bash
docker build -t my-flask-app .
```

### **Step 3: Run the Docker Container**

```bash
docker run -p 5000:5000 my-flask-app
```

Access the app at **[http://localhost:5000/](http://localhost:5000/)**.

---

## **Part 3: Pushing the Docker Image to AWS ECR**

### **Step 1: Create an ECR Repository**

Create an **Amazon ECR repository** using Python **Boto3**:

```python
import boto3

ecr_client = boto3.client('ecr')
repository_name = 'my-ecr-repo'
response = ecr_client.create_repository(repositoryName=repository_name)
print(response['repository']['repositoryUri'])
```

### **Step 2: Push the Docker Image to ECR**

```bash
docker tag my-flask-app <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-ecr-repo:latest
docker push <aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-ecr-repo:latest
```

---

## **Part 4: Deploying on Amazon EKS**

### **Step 1: Create an EKS Cluster**

Create an **EKS cluster** and add a **node group**.

### **Step 2: Deploy the App using Kubernetes Python Client**

```python
from kubernetes import client, config

# Load Kubernetes configuration
config.load_kube_config()
api_client = client.ApiClient()

# Define the Deployment
deployment = client.V1Deployment(
    metadata=client.V1ObjectMeta(name="my-flask-app"),
    spec=client.V1DeploymentSpec(
        replicas=1,
        selector=client.V1LabelSelector(match_labels={"app": "my-flask-app"}),
        template=client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "my-flask-app"}),
            spec=client.V1PodSpec(
                containers=[
                    client.V1Container(
                        name="my-flask-container",
                        image="<aws_account_id>.dkr.ecr.us-east-1.amazonaws.com/my-ecr-repo:latest",
                        ports=[client.V1ContainerPort(container_port=5000)]
                    )
                ]
            )
        )
    )
)

# Deploy to Kubernetes
api_instance = client.AppsV1Api(api_client)
api_instance.create_namespaced_deployment(namespace="default", body=deployment)

# Define the Service
service = client.V1Service(
    metadata=client.V1ObjectMeta(name="my-flask-service"),
    spec=client.V1ServiceSpec(
        selector={"app": "my-flask-app"},
        ports=[client.V1ServicePort(port=5000)]
    )
)

# Create the Service
api_instance = client.CoreV1Api(api_client)
api_instance.create_namespaced_service(namespace="default", body=service)
```

Make sure to **replace `<aws_account_id>`** with your actual AWS account ID.

### **Step 3: Verify Deployment**
Run the following commands:

```bash
kubectl get deployment -n default  # Check deployment status
kubectl get service -n default     # Check service
kubectl get pods -n default        # Check running pods
```

### **Step 4: Expose the Service**
If the service is not externally accessible, use port forwarding:

```bash
kubectl port-forward service/my-flask-service 5000:5000
```

Now, access the application at **[http://localhost:5000/](http://localhost:5000/)**.

---

## **Conclusion** 🎉

By following this guide, you have:
 Built a **Cloud-Native Resource Monitoring App** using Python and Flask.  
 Containerized the app using **Docker** and pushed the image to **AWS ECR**.  
 Deployed the app on **Amazon EKS** using **Kubernetes manifests and Python client**.  




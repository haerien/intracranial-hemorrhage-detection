# Intracranial Hemorrhage Detection

This project is a web application that uses a pre-trained Hugging Face model to detect types of brain hemorrhage from medical images. It has been deployed using Docker and AWS to ensure scalability and ease of access.

Live: http://3.79.8.171:8000/

## Features

- Uses a pre-trained model to classify and identify types of intracranial hemorrhages from uploaded images.
- Containerized application for consistent and reproducible deployment.
- Deployed on AWS for high availability and reliability.

## Getting Started

### Prerequisites

- Docker
- AWS Account

### Setup and Deployment

1. **Clone the Repository**
   ```bash
   git clone https://github.com/haerien/brain-hemorrhage-detection.git
   cd brain-hemorrhage-detection
   ```

2. **Build the Docker Image**
   ```bash
   docker build -t brain-hemorrhage-detection .
   ```

3. **Run the Docker Container Locally (Optional)**
   ```bash
   docker run -it -p 8000:8000 brain-hemorrhage-detection
   ```
    Access the application at **http://localhost:8000**

4. **Deploy to AWS**
   * **Configure AWS if you haven't did this before**
     ```bash
     aws configure
     ```
     ❗ Make sure you enter your **AWS Access Key ID** and **AWS Secret Access Key** correct.

   * **Create an ECR Repository**
     ```bash
     aws ecr create-repository --repository-name brain-hemorrhage-detection --region [<your-region>]
     ```
     ❗ If you encounter an **AccessDeniedException** error, ensure that you have created a user and granted it **AmazonEC2ContainerRegistryFullAccess** permissions.
     
   * **Authenticate Docker to ECR**
     ```bash
     aws ecr get-login-password --region [<your-region>] | docker login --username AWS --password-stdin[<your-aws-account-id>].dkr.ecr.[<your-region>].amazonaws.com
     ```
     
   * **Tag and Push Your Image**
       ```bash
       docker tag brain-hemorrhage-detection [<your-aws-account-id>].dkr.ecr.[<your-region>].amazonaws.com/brain-hemorrhage-detection
       docker push [<your-aws-account-id>].dkr.ecr.[<your-region>].amazonaws.com/brain-hemorrhage-detection
       ```
       
   * **Create a Cluster**
       ```bash
       aws ecs create-cluster --cluster-name brain-hemorrhage-cluster --region [<your-region>]
       ```
       ❗ Again, if you encounter **AccessDeniedException** error, make sure you granted the right permissions.
       
   * **Register task definition**
       ```bash
       aws ecs register-task-definition --cli-input-json file://task-definition.json
       ```
   * **Run the Task on ECS**
       ```bash
       aws ecs create-service --cluster brain-hemorrhage-cluster --service-name brain-hemorrhage-service --task-definition brain-hemorrhage-task --desired-count 1 --launch-type FARGATE --network-configuration "awsvpcConfiguration={subnets=[<your-subnet-id>],securityGroups=[<your-security-group-id>],assignPublicIp=ENABLED}" --region [<your-region>]
       ```
       Well... That code might look a bit scary
     ### **To find your subnet ID:**
     * **1)** Sign in to the AWS Management Console.
     * **2)** Navigate to the VPC Dashboard:
        * In the AWS Management Console, search for "VPC" and select the VPC service.
     * **3)** View Subnets:
        *  In the left-hand menu, click on "Subnets".
        *  Find the subnet you want to use. Ensure it's in the same region.
        *  Note the Subnet ID (e.g., 'subnet-12345678').
     ### **To find your security group ID:**
     * **1)** Navigate to the EC2 Dashboard:
        *  In the AWS Management Console, search for "EC2" and select the EC2 service.
     * **2)** View Security Groups:
        *  In the left-hand menu, click on "Security Groups".
        *  Find the security group you want to use or create a new one if necessary.
        *  Note the Security Group ID (e.g., 'sg-12345678').
5. **Enjoy!**
   * Find the public IP of your task, add port "8000" to the end of it and start using.

### Usage
  * Upload an Image
    Navigate to the web application and use the upload feature to submit a medical image.
  * Get Predictions
    After uploading, the model will process the image and return the type of brain hemorrhage detected.

### Contributing
  Feel free to open issues or submit pull requests if you have improvements or bug fixes.
  1) Fork the repository.
  2) Create a new branch (git checkout -b feature/your-feature).
  3) Make your changes and commit (git commit -am 'Add new feature').
  4) Push to the branch (git push origin feature/your-feature).
  5) Create a new Pull Request.

### Acknowledgements
  * The model used in this project is <a href="https://huggingface.co/DifeiT/rsna-intracranial-hemorrhage-detection">rsna-intracranial-hemorrhage-detection by DifeiT.<a>
       

For detailed deployment instructions, refer to the <a href="https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html">AWS documentation<a>.

```
Feel free to adjust any details if needed!
```

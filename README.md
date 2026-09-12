# Contact-Book
# Containerized Contact Book — 3-Tier Enterprise Cloud Architecture on AWS

An enterprise-grade, highly available, and auto-scaling three-tier web application deployed in the AWS Africa (Cape Town) region (`af-south-1`). 

The architecture hosts a containerized Python/Flask Contact Book service with Nginx reverse proxying, fronted by an Application Load Balancer (ALB), managed inside an Auto Scaling Group (ASG) across multiple Availability Zones, with persistence on Amazon RDS PostgreSQL. Deployments are fully automated via GitHub Actions utilizing a custom zero-downtime Blue/Green deployment strategy executed over AWS Systems Manager (SSM).

---

## 🔗 Architecture Repositories

To enforce strict separation of concerns between application code, deployment pipelines, and cloud provisioning, this project is split into two specialized repositories:

* **Application & CI/CD Pipeline Repository (This Repo):** Contains the Flask application, frontend assets, database connection pooling logic, Docker specifications, and GitHub Actions Blue/Green deployment workflows.
* **Infrastructure as Code (Terraform) Repository:** [AWS 3-Tier VPC, ALB, ASG & RDS Infrastructure]([https://github.com/sereromokwena/aws-3tier-terraform-infra](https://github.com/Serero-Codes/contact-Book-infrastructure)). Contains the complete modular Terraform state managing the VPC, subnets, route tables, security group isolation, IAM roles, launch templates, and PostgreSQL RDS instances.

---

## 🏛️ System Architecture

```text
                                  INTERNET
                                     │
                             [ Internet Gateway ]
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
          Public Subnet 1 (af-south-1a)   Public Subnet 2 (af-south-1b)
          ┌───────────────────────────┐   ┌───────────────────────────┐
          │     NAT Gateway (EIP)     │   │                           │
          │                           │   │                           │
          │  ┌─────────────────────┐  │   │  ┌─────────────────────┐  │
          │  │  ALB Node (Port 80) │  │   │  │  ALB Node (Port 80) │  │
          │  └──────────┬──────────┘  │   │  └──────────┬──────────┘  │
          └─────────────┼─────────────┘   └─────────────┼─────────────┘
                        └───────────────┬───────────────┘
                                        │ (HTTP Traffic)
                     ┌──────────────────┴──────────────────┐
                     ▼                                     ▼
          Private Subnet 1 (af-south-1a)   Private Subnet 2 (af-south-1b)
          ┌───────────────────────────┐    ┌───────────────────────────┐
          │  EC2 (Target Group: 80)   │    │  EC2 (Target Group: 80)   │
          │  ┌─────────────────────┐  │    │  ┌─────────────────────┐  │
          │  │ Nginx (Reverse Proxy│  │    │  │ Nginx (Reverse Proxy│  │
          │  └──────────┬──────────┘  │    │  └──────────┬──────────┘  │
          │             │ (:8081/8082)│    │             │ (:8081/8082)│
          │  ┌──────────▼──────────┐  │    │  ┌──────────▼──────────┐  │
          │  │ Docker (Flask App)  │  │    │  │ Docker (Flask App)  │  │
          │  └──────────┬──────────┘  │    │  └──────────┬──────────┘  │
          └─────────────┼─────────────┘    └─────────────┼─────────────┘
                        └────────────────┬───────────────┘
                                         │ (TCP Port 5432)
                                         ▼
                               [ Database Subnet Group ]
                           ┌───────────────────────────────┐
                           │   Amazon RDS PostgreSQL 15    │
                           │   Engine: db.t3.micro (appdb) │
                           └───────────────────────────────┘



# Containerized Contact Book — 3-Tier Enterprise Cloud Architecture on AWS

An enterprise-grade, highly available, and auto-scaling three-tier web application deployed in the AWS Africa (Cape Town) region (`af-south-1`). 

The system runs a containerized Python Flask application behind an Nginx reverse proxy on private EC2 instances within an Auto Scaling Group (ASG), load-balanced across multiple Availability Zones via an Application Load Balancer (ALB), with persistent storage on Amazon RDS PostgreSQL. Continuous Integration and Continuous Deployment (CI/CD) is fully automated with GitHub Actions, executing zero-downtime Blue/Green container cutovers via AWS Systems Manager (SSM).

---

## 🔗 Architecture Repositories

To enforce separation of concerns between application code, deployment automation, and cloud provisioning, this project is split across two dedicated repositories:

* **Application & CI/CD Pipeline Repository (This Repo):** Contains the Flask application, frontend static assets, database connection pooling logic, Docker specifications, and GitHub Actions Blue/Green deployment workflows.
* **Infrastructure as Code (Terraform) Repository:** [AWS 3-Tier VPC, ALB, ASG & RDS Infrastructure](https://github.com/sereromokwena/aws-3tier-terraform-infra) — Contains the modular Terraform configurations managing the VPC, public/private subnets, NAT Gateway, security groups, IAM instance profiles, launch templates, Auto Scaling Group, and PostgreSQL RDS instances.

---

## 🏛️ System Architecture

```text
                                  INTERNET
                                     │
                             [ Internet Gateway ]
                                     │
                     ┌───────────────┴───────────────┐
                     ▼                               ▼
          Public Subnet 1 (af-south-1a)   Public Subnet 2 (af-south-1b)
          ┌───────────────────────────┐   ┌───────────────────────────┐
          │     NAT Gateway (EIP)     │   │                           │
          │                           │   │                           │
          │  ┌─────────────────────┐  │   │  ┌─────────────────────┐  │
          │  │  ALB Node (Port 80) │  │   │  │  ALB Node (Port 80) │  │
          │  └──────────┬──────────┘  │   │  └──────────┬──────────┘  │
          └─────────────┼─────────────┘   └─────────────┼─────────────┘
                        └───────────────┬───────────────┘
                                        │ (HTTP Traffic)
                     ┌──────────────────┴──────────────────┐
                     ▼                                     ▼
          Private Subnet 1 (af-south-1a)   Private Subnet 2 (af-south-1b)
          ┌───────────────────────────┐    ┌───────────────────────────┐
          │  EC2 (Target Group: 80)   │    │  EC2 (Target Group: 80)   │
          │  ┌─────────────────────┐  │    │  ┌─────────────────────┐  │
          │  │ Nginx (Reverse Proxy│  │    │  │ Nginx (Reverse Proxy│  │
          │  └──────────┬──────────┘  │    │  └──────────┬──────────┘  │
          │             │ (:8081/8082)│    │             │ (:8081/8082)│
          │  ┌──────────▼──────────┐  │    │  ┌──────────▼──────────┐  │
          │  │ Docker (Flask App)  │  │    │  │ Docker (Flask App)  │  │
          │  └──────────┬──────────┘  │    │  └──────────┬──────────┘  │
          └─────────────┼─────────────┘    └─────────────┼─────────────┘
                        └────────────────┬───────────────┘
                                         │ (TCP Port 5432)
                                         ▼
                               [ Database Subnet Group ]
                           ┌───────────────────────────────┐
                           │   Amazon RDS PostgreSQL 15    │
                           │   Engine: db.t3.micro (appdb) │
                           └───────────────────────────────┘
```

---

## 🛡️ Key Architectural Pillars

### 1. Network Isolation & Security Group Chaining
* **Zero Public IP Compute:** EC2 application nodes reside exclusively in **Private Subnets** (`10.0.10.0/24` and `10.0.20.0/24`) with no public IP addresses assigned.
* **Strict Security Group Referencing:**
  * `alb-sg`: Permits inbound HTTP traffic on port `80` from `0.0.0.0/0`.
  * `web-sg`: Restricts inbound port `80` traffic solely to traffic originating from `alb-sg`.
  * `db-sg`: Restricts inbound PostgreSQL traffic on port `5432` strictly to instances assigned `web-sg`.
* **NAT Gateway Egress:** Outbound internet access from private nodes (for Docker image pulls, security updates, and OS packages) routes through a managed NAT Gateway located in public subnet `af-south-1a`.
* **Zero Inbound SSH:** Port `22` is completely closed across all security groups. Remote administration, maintenance, and deployments are brokered via IAM policies and **AWS Systems Manager (SSM)**.

### 2. High Availability & Auto-Healing
* **Multi-AZ Distribution:** The Auto Scaling Group balances nodes across `af-south-1a` and `af-south-1b` with a capacity boundary of **Min: 2**, **Desired: 2**, and **Max: 4**.
* **ELB Health Checks:** The Target Group continuously polls the root route (`/`) every 30 seconds. If an instance degrades or fails, the ASG automatically terminates the node and launches a healthy replacement.
* **Launch Template Self-Healing:** The `user_data` script in `aws_launch_template.web` completely provisions new instances on boot, eliminating Apache conflicts, configuring Nginx, and starting the Docker container connected to RDS immediately.

---

## 🛠️ Technology Stack

* **Backend:** Python 3.11, Flask, Gunicorn, `psycopg2-binary` (Threaded Connection Pooling)
* **Frontend:** Semantic HTML5, CSS3 Variables, Vanilla JavaScript (Fetch API)
* **Reverse Proxy:** Nginx (listening on port `80`, proxying to loopback ports `8081` / `8082`)
* **Containerization:** Docker Engine, Docker Buildx, Docker Hub Registry
* **Infrastructure as Code (IaC):** Terraform (`>= 1.5.0`), HashiCorp AWS Provider (`~> 5.0`)
* **CI/CD Pipeline:** GitHub Actions, AWS CLI v2, AWS Systems Manager (SSM Run Command)
* **Cloud Infrastructure:** AWS VPC, ALB, Auto Scaling Groups, EC2, RDS PostgreSQL, NAT Gateway, CloudWatch

---

## 🔄 Zero-Downtime Blue/Green Deployment Workflow

Deployments run in-place on each EC2 instance by alternating active container colors, verifying application health, and reloading Nginx without dropping TCP connections.

```text
       Incoming HTTP Traffic (:80)
                   │
                   ▼
       ┌────────────────────────┐
       │   Nginx Reverse Proxy  │
       └───────────┬────────────┘
                   │
         [ Current Traffic: 8081 ]
                   │
       ┌───────────▼────────────┐        ┌────────────────────────┐
       │   app-blue (ACTIVE)    │        │    app-green (IDLE)    │
       │   Port 8081 (v1.0.0)   │        │   Port 8082 (Deploying)│
       └────────────────────────┘        └────────────────────────┘
                   │                                  │
                   │ 1. Pull new Docker image         │
                   │ 2. Boot container on Port 8082 ──┘
                   │ 3. Run internal loopback health checks
                   │ 4. Reconfigure Nginx proxy_pass -> :8082
                   │ 5. Reload Nginx without drop (`nginx -s reload`)
                   ▼
       ┌────────────────────────┐
       │   Nginx Reverse Proxy  │
       └───────────┬────────────┘
                   │
         [ Swapped Traffic: 8082 ]
                   │
       ┌────────────────────────┐        ┌────────────────────────┐
       │    app-blue (DRAIN)    │        │   app-green (ACTIVE)   │
       │ 6. Stop & prune        │        │   Port 8082 (v1.1.0)   │
       └────────────────────────┘        └────────────────────────┘
```

### Deployment Pipeline Step-by-Step

1. **Trigger:** A developer pushes code changes to the `main` branch.
2. **Build & Tag:** GitHub Actions compiles the image using Docker Buildx, tagging the build with both `latest` and `${{ github.sha }}`, and pushes it to Docker Hub.
3. **Dynamic Target Discovery:** The pipeline dispatches an AWS SSM command using tag-based targeting (`--targets "Key=tag:Name,Values=asg-web-instance"`). All current ASG nodes receive the command concurrently, preventing deployment failures caused by instance turnover.
4. **Active Color Detection:** The script inspects `docker ps` to determine the current container:
   * If `app-blue` (:8081) is active, the deploy target is `app-green` (:8082).
   * If `app-green` (:8082) is active, the deploy target is `app-blue` (:8081).
5. **Pre-Flight Health Verification:** The new container starts on the standby port. The deployment script polls `http://127.0.0.1:<NEW_PORT>/` up to 15 times (every 3 seconds). If the container crashes or fails to connect to RDS, the workflow aborts, keeping the existing container online.
6. **Traffic Cutover:** Upon health check success, `sed` updates `/etc/nginx/conf.d/app.conf` to point to the new port, and `nginx -s reload` shifts traffic seamlessly.
7. **Drain & Prune:** The older container is stopped and removed, and untagged images are pruned to conserve disk space.

---

## 🗄️ Database Architecture & Connection Pooling

Persistence is managed via Amazon RDS PostgreSQL 15, isolated within a private DB Subnet Group.

* **Engine:** PostgreSQL 15 (`db.t3.micro`)
* **Database Name:** `appdb`
* **Master User:** `dbadmin`
* **Port:** `5432`

### Schema Definition
```sql
CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Thread-Safe Connection Pool (`db.py`)
To eliminate connection exhaustion and socket starvation under load, connection acquisition is managed using `ThreadedConnectionPool`:

```python
import os
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor

db_pool = ThreadedConnectionPool(
    minconn=1,
    maxconn=20,
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT", "5432"),
    dbname=os.environ.get("DB_NAME", "appdb"),
    user=os.environ.get("DB_USER", "dbadmin"),
    password=os.environ.get("DB_PASSWORD")
)

def get_db_connection():
    return db_pool.getconn()

def release_db_connection(conn):
    db_pool.putconn(conn)
```

---

## ⚙️ Configuration & Environment Variables

| Variable | Description | Production / Example Value |
| :--- | :--- | :--- |
| `DB_HOST` | RDS PostgreSQL Endpoint | `terraform-*.cfgcmswsckgz.af-south-1.rds.amazonaws.com` |
| `DB_PORT` | PostgreSQL Port | `5432` |
| `DB_NAME` | Database Name | `appdb` |
| `DB_USER` | Master Database Username | `dbadmin` |
| `DB_PASSWORD` | Master Database Password | Secure string stored in GitHub Secrets |
| `PORT` | Container Internal Listening Port | `5000` |

---

## 🔐 Required GitHub Secrets

Configure the following secrets in your GitHub repository (**Settings > Secrets and variables > Actions**):

* `AWS_ACCESS_KEY_ID`: IAM access key with permissions for `ssm:SendCommand` and `ssm:ListCommandInvocations`.
* `AWS_SECRET_ACCESS_KEY`: IAM secret key.
* `AWS_REGION`: Target AWS deployment region (`af-south-1`).
* `DOCKERHUB_USERNAME`: Docker Hub namespace / username.
* `DOCKERHUB_TOKEN`: Docker Hub Personal Access Token.
* `DB_HOST`: Amazon RDS PostgreSQL endpoint hostname.
* `DB_PORT`: `5432`
* `DB_NAME`: `appdb`
* `DB_USER`: `dbadmin`
* `DB_PASSWORD`: Master password for PostgreSQL instance.

---

## 🚀 Bootstrap & Launch Template Automation

To ensure any replacement instance created by the Auto Scaling Group initializes cleanly with Docker, Nginx, and the live application, the `aws_launch_template.web` resource runs this script within `user_data`:

```bash
#!/bin/bash
set -ex

# 1. Disable conflicting web servers present on base AMI
systemctl stop apache2 || true
systemctl disable apache2 || true

# 2. Install Docker runtime and Nginx
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y docker.io nginx curl
systemctl enable --now docker
usermod -aG docker ubuntu

# 3. Configure Nginx reverse proxy to container port 8081
cat > /etc/nginx/conf.d/app.conf << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass [http://127.0.0.1:8081](http://127.0.0.1:8081);
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
rm -f /etc/nginx/sites-enabled/default || true
nginx -t
systemctl restart nginx
systemctl enable nginx

# 4. Pull and run the application container connected to RDS
docker pull sereromokwena/my-app:latest
docker run -d \
  --name app-blue \
  -p 8081:5000 \
  -e DB_HOST="${aws_db_instance.postgres.address}" \
  -e DB_PORT="5432" \
  -e DB_NAME="${aws_db_instance.postgres.db_name}" \
  -e DB_USER="${aws_db_instance.postgres.username}" \
  -e DB_PASSWORD="${aws_db_instance.postgres.password}" \
  --restart unless-stopped \
  sereromokwena/my-app:latest
```

---

## 🧪 Operational Testing & Verification

Run these AWS CLI commands to verify cluster health and data operations end-to-end:

### 1. Verify Target Group Health
```bash
TG_ARN=$(aws elbv2 describe-target-groups --region af-south-1 --query "TargetGroups[0].TargetGroupArn" --output text)
aws elbv2 describe-target-health --region af-south-1 --target-group-arn "$TG_ARN" --output table
```
*Expected Result: Both instances report `healthy` on port 80.*

### 2. Verify Load Balancing Across Availability Zones
```bash
for i in {1..10}; do
  curl -s -o /dev/null -w "%{http_code}\n" [http://main-alb-1095085319.af-south-1.elb.amazonaws.com](http://main-alb-1095085319.af-south-1.elb.amazonaws.com)
done
```
*Expected Result: Ten consecutive HTTP `200` responses.*

### 3. Test Contact Creation & Persistence (POST API)
```bash
curl -i -X POST [http://main-alb-1095085319.af-south-1.elb.amazonaws.com/api/contacts](http://main-alb-1095085319.af-south-1.elb.amazonaws.com/api/contacts) \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Sipho",
    "last_name": "Dlamini",
    "phone_number": "0831234567",
    "email": "sipho@example.co.za"
  }'
```
*Expected Result: HTTP `201 CREATED` returning the stored JSON record with generated primary key ID.*

### 4. Fetch All Contacts (GET API)
```bash
curl -i [http://main-alb-1095085319.af-south-1.elb.amazonaws.com/api/contacts](http://main-alb-1095085319.af-south-1.elb.amazonaws.com/api/contacts)
```
*Expected Result: HTTP `200 OK` returning the array of stored contacts.*

---

## 📊 CloudWatch & Monitoring Strategy

### Out-of-the-Box Metrics
* **Application Load Balancer:** `RequestCount`, `TargetResponseTime`, `HTTPCode_Target_2XX_Count`, `HTTPCode_Target_5XX_Count`, `UnHealthyHostCount`
* **Amazon RDS PostgreSQL:** `CPUUtilization`, `FreeableMemory`, `DatabaseConnections`, `ReadLatency`, `WriteLatency`
* **Auto Scaling Group & EC2:** Hypervisor-level CPU utilization, network I/O, and disk metrics

### Containerized Telemetry (Production Add-on)
Application container logs can be streamed directly to CloudWatch Log Groups by attaching the `CloudWatchAgentServerPolicy` managed policy to `ec2-ssm-role` and specifying `--log-driver=awslogs` during container execution:

```bash
--log-driver=awslogs \
--log-opt awslogs-region="af-south-1" \
--log-opt awslogs-group="/aws/ec2/contact-book" \
--log-opt awslogs-create-group="true" \
--log-opt awslogs-stream="contact-book-$(hostname)"
```

---

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

# Data Pipeline Project - Terrific Totes

## Overview
Terrific Totes, a fictional company, operates an OLTP database and a data warehouse used for reporting and visualizations. The goal of this project is to develop applications that Extract, Transform, and Load (ETL) data from the OLTP database into a data lake and warehouse hosted in AWS. This solution is reliable, resilient, and fully managed using Infrastructure-as-Code (Terraform, Python, GitHub Actions, and Makefile).

## Features
- **Automated Data Processing**
  - **EventBridge Scheduler**: Triggers data ingestion every 5 minutes.
  - **Step Machine with JSON Payloads**: Orchestrates the workflow.
  - **Lambda Functions & Layers**: 
    - One Python application ingests all tables from the `totesys` database.
    - Another application remodels some data into a predefined schema and stores it in the "processed" S3 bucket in Parquet format.
    - A third application loads the transformed data into a data warehouse at defined intervals.
- **CloudWatch Monitoring & SNS Alerts**
  - Logs errors, tracks performance, and sends critical failure notifications via SNS.
- **Secure Data Management**
  - **IAM Policies**: Implements the principle of least privilege.
  - **Secrets Manager**: Manages database credentials securely.
- **Data Storage in S3**
  - **Raw Data Bucket**: Stores ingested data in its original form.
  - **Processed Data Bucket**: Holds transformed data in an immutable, well-structured format.
- **Code Quality & Security**
  - Python code is **PEP8 compliant**, thoroughly tested, and checked for security vulnerabilities using `pip-audit` and `bandit`.

## Architecture
![Architecture Diagram](architecture.png)  

## Tech Stack
- **Infrastructure & CI/CD**: Terraform, GitHub Actions, Makefile
- **Programming & Libraries**: Python, boto3, pandas, numpy, pg8000
- **AWS Services**: CloudWatch, Lambda, EventBridge, Step Functions, SNS, S3, Secrets Manager
- **Development Tools**: Visual Studio Code, Tableau

## Installation & Setup
1. **Create an AWS Account** and configure AWS credentials.
2. **Fork and Clone the Repository**
   ```sh
   git clone https://github.com/ys218279/team-09-sperrins.git
   cd team-09-sperrins
   ```
3. **Set Up Databases**
   - Create source and target databases from the provided ERD.
4. **Install Terraform** (if not already installed)
5. **Set Up Terraform Backend**
   - Create an S3 bucket to store Terraform state files.
6. **Run Makefile Commands**
   ```sh
   make all  # Creates virtual environment, installs dependencies, formats code, runs security and test coverage checks
   ```
7. **Configure Sensitive Variables**
   - Create a `sensitive.tfvars` file with database credentials and SNS email.
   - Store AWS credentials, database credentials, and SNS email in GitHub secrets.
8. **Deploy Infrastructure**
   ```sh
   terraform init
   terraform plan -var-file=sensitive.tfvars
   terraform apply -var-file=sensitive.tfvars
   ```
   *(If deploying via GitHub Actions, this step can be automated.)*

## Folder Structure
```
/your-repo
|-- data/                # Raw and processed data
|-- src/                 # Source code for the pipeline
|   |-- ingestion/       # Scripts for data extraction
|   |-- processing/      # Data transformation scripts
|   |-- storage/         # Data storage logic
|-- logs/                # Logging output
|-- config/              # Configuration files
|-- tests/               # Unit and integration tests
|-- requirements.txt     # Project dependencies
|-- README.md            # Documentation
```

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License
This project is licensed under the [Your License] License. See `LICENSE` for details.

## Contact
For any questions or issues, reach out via [GitHub Issues](https://github.com/ys218279/team-09-sperrins/issues).

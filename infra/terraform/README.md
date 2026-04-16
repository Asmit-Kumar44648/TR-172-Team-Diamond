# GRASP Infrastructure Setup (Terraform)

Follow these steps to provision the production environment for GRASP on Google Cloud Platform.

## 10 Steps to Production Launch

1.  **GCP Project**: Create a new project named `grasp-platform` in the GCP Console.
2.  **Enabled APIs**: Enable the following APIs: Cloud Run, Secret Manager, Cloud Storage, and Artifact Registry.
3.  **Local Auth**: Ensure you have the Google Cloud SDK installed and run `gcloud auth application-default login`.
4.  **Init Terraform**: From this directory, run `terraform init`.
5.  **Plan**: Run `terraform plan -var="project_id=YOUR_PROJECT_ID"` to preview the resource creation.
6.  **Apply**: Run `terraform apply -var="project_id=YOUR_PROJECT_ID"`.
7.  **Populate Secrets**: Go to the Google Secret Manager console and create versions for each of the secrets (e.g., `anthropic-key`) with your actual API keys.
8.  **Internal SDK**: Run the `deploy-modal` step manually or via CI once the secrets are ready.
9.  **GitHub Secret**: Download the `grasp-deployer` service account key (JSON) and save it as a GitHub Repository Secret named `GOOGLE_CREDENTIALS`.
10. **Push to Main**: Push your changes to the `main` branch to trigger the first automated production deployment.

## Troubleshooting
- **IAM Permission propagation**: It can take up to 2 minutes for new IAM roles to propagate. If the first CI build fails on `gcloud run deploy`, wait a moment and retry.
- **Quota**: Ensure your GCP project has billing enabled to provision Cloud Run instances and GCS buckets.

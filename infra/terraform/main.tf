provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP Region"
  type        = string
  default     = "us-central1"
}

# 1. Cloud Run Service for the API
resource "google_cloud_run_v2_service" "grasp_api" {
  name     = "grasp-api"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "gcr.io/${var.project_id}/grasp-api:latest"
      
      resources {
        limits = {
          cpu    = "1"
          memory = "2Gi"
        }
      }

      # Secrets placeholders (values managed via Secret Manager)
      env {
        name = "ANTHROPIC_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "anthropic-key"
            version = "latest"
          }
        }
      }
      # ... repeat for other secrets (SUPABASE, REDIS, etc)
    }
    
    scaling {
      max_instance_count = 3
      min_instance_count = 0
    }
  }
}

# 2. Storage Buckets
resource "google_storage_bucket" "scenes" {
  name          = "grasp-scenes-${var.project_id}"
  location      = "US"
  force_destroy = false
}

resource "google_storage_bucket" "results" {
  name          = "grasp-results-${var.project_id}"
  location      = "US"
  force_destroy = false
}

# 3. Secret Manager Setup (Names only)
resource "google_secret_manager_secret" "secrets" {
  for_each = toset([
    "anthropic-key", "db-url", "redis-url", "supabase-key", 
    "stripe-key", "stripe-webhook"
  ])
  secret_id = each.key
  replication {
    auto {}
  }
}

# 4. Service Account for CI/CD and Cloud Run
resource "google_service_account" "grasp_deployer" {
  account_id   = "grasp-deployer"
  display_name = "GRASP Deployer Service Account"
}

# IAM Roles
resource "google_project_iam_member" "deployer_roles" {
  for_each = toset([
    "roles/run.admin",
    "roles/storage.objectAdmin",
    "roles/secretmanager.secretAccessor",
    "roles/iam.serviceAccountUser",
    "roles/artifactregistry.admin"
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.grasp_deployer.email}"
}

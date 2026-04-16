# GRASP — Grasp Risk Audit and Safety Pre-flight System

GRASP is a production SaaS platform for robotics engineers to audit robot grasps before execution using Contact-GraspNet inference, G-SAFE reranking, and multi-agent validation. It provides a REST API, real-time job tracking, and a web dashboard for reviewing ranked grasp plans against benchmark-quality collision metrics. The platform is multi-tenant, Stripe-billed, and deploys inference workloads on Modal serverless GPUs.

---

## Local Dev Setup

1. **Clone the repo and enter the project root**
   ```bash
   git clone <repo-url> grasp-platform
   cd grasp-platform
   ```

2. **Copy and fill environment variables**
   ```bash
   cp .env.example .env
   # Edit .env — fill DATABASE_URL, REDIS_URL, Supabase keys, etc.
   ```

3. **Start all services with Docker Compose**
   ```bash
   docker compose up --build
   ```
   Postgres initialises from `packages/schema/migrations/001_initial.sql` automatically.

4. **Verify services are running**
   | Service  | URL                        |
   |----------|----------------------------|
   | API      | http://localhost:8000      |
   | Web      | http://localhost:3000      |
   | Postgres | localhost:5432             |
   | Redis    | localhost:6379             |

5. **Run schema package tests (Python)**
   ```bash
   cd packages/schema
   pip install -r requirements.txt
   python -c "from models import ScenePlan; print('Schema OK')"
   ```

---

## App Structure

| Path | Purpose |
|------|---------|
| [`apps/api/`](./apps/api) | FastAPI backend — REST endpoints, auth middleware, job dispatch |
| [`apps/web/`](./apps/web) | Next.js 14 dashboard — scene upload, job monitor, grasp viewer |
| [`apps/worker/`](./apps/worker) | Celery / Modal worker — inference pipeline execution |
| [`packages/pipeline/`](./packages/pipeline) | Core inference logic — Contact-GraspNet + G-SAFE |
| [`packages/schema/`](./packages/schema) | Pydantic models + Alembic SQL migrations |
| [`packages/agents/`](./packages/agents) | Multi-agent audit resolvers |
| [`infra/terraform/`](./infra/terraform) | Cloud infrastructure — GCS, Cloud Run, networking |
| [`infra/docker/`](./infra/docker) | Shared Dockerfiles and base images |
| [`ml/demo_scenes/`](./ml/demo_scenes) | Sample `.npz` depth/RGB scene files for testing |

---

## Deployment Stack

| Variable | Purpose |
|----------|---------|
| `DATABASE_URL` | Supabase Postgres connection string |
| `REDIS_URL` | Upstash Redis (job queues) |
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Supabase service role key (server-side) |
| `SUPABASE_ANON_KEY` | Supabase anon key (client-side) |
| `ANTHROPIC_API_KEY` | Claude API for agent reasoning |
| `STRIPE_SECRET_KEY` | Stripe billing |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signature verification |
| `MODAL_TOKEN_ID` | Modal.com GPU worker token |
| `MODAL_TOKEN_SECRET` | Modal.com GPU worker secret |
| `GCS_BUCKET_SCENES` | GCS bucket — uploaded scene files |
| `GCS_BUCKET_RESULTS` | GCS bucket — analysis result JSON |
| `ALLOWED_ORIGINS` | CORS allow-list for the API |
| `NEXT_PUBLIC_API_URL` | API base URL (client-side) |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase URL (client-side) |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key (client-side) |

---

## Architecture Overview

```
Browser / SDK
     │
     ▼
Next.js 14 (Vercel) ──► FastAPI (Cloud Run)
                              │
                    ┌─────────┴──────────┐
                    ▼                    ▼
             Supabase DB          Modal GPU Worker
             (Postgres + RLS)     (Contact-GraspNet)
                    │                    │
                    └────── GCS ─────────┘
                         (scenes + results)
```

---

## Phase Roadmap

- [x] Phase 1 — Monorepo scaffold + schema + DB migrations
- [x] Phase 2 — FastAPI backend (auth, scenes, jobs endpoints)
- [x] Phase 3 — Inference pipeline (Contact-GraspNet + G-SAFE)
- [x] Phase 4 — Next.js web dashboard
- [x] Phase 5 — Standardized Free Tier & Safety Quotas (Billing Removed)
- [x] Phase 6 — Multi-agent audit resolvers (Claude-4 Integration)
- [x] Phase 7 — Terraform infra + CI/CD
- [x] Phase 8 — Rebranding (Industrial Gold/Amber theme)

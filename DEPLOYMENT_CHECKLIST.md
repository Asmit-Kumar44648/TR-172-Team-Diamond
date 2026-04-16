# GRASP Final Deployment Checklist

Verify each item before marking the platform ready for production traffic.

## Pre-deployment
- [ ] All `pytest` tests pass in `apps/api` and `packages/`
- [ ] All `lint` and `tsc` checks pass in `apps/web`
- [ ] `demo_cluttered.npz` triggers Type-O rejection on rank-1 (Safety Gate Check)
- [ ] G-SAFE ranking differs from raw Contact-GraspNet in ≥2 of top-5 positions (Value Add Check)
- [ ] All scores confirmed in [0.0, 1.0] range
- [ ] `ScenePlan` validates against Pydantic schema

## Environment
- [ ] All secrets in Google Secret Manager (zero secrets in source code/env files)
- [ ] Supabase RLS policies applied (No public access to raw scenes)
- [ ] Upstash Redis connected + rate limits tested
- [ ] Modal GPU worker deployed + warm test complete
- [ ] Vercel production environment variables set

## Security
- [ ] `ANTHROPIC_API_KEY` never appears in logs, browser network tab, or frontend bundle
- [ ] API keys shown exactly once on creation (No recovery possible)
- [ ] Webhook HMAC signature verification tested in `v1/webhooks`
- [ ] File upload magic byte validation tested (Reject non-NPZ/NPY files)
- [ ] Rate limiting tested (1001st free-tier request returns 429)

## Product
- [ ] 3D viewer renders scene point cloud and grasp spheres correctly
- [ ] Rejection card appears for cluttered/dangerous demo scenes
- [ ] SSE stream updates UI in real-time (No manual refresh needed)
- [ ] ROS JSON export validates against MoveIt schema
- [ ] Benchmark table shows current platform performance (73.6% / 63.4%)
- [ ] "Share" button generates functional read-only analysis URLs

## Deployment
- [ ] Cloud Run `min-instances=0` (verified scaling to zero cost)
- [ ] GitHub Actions pipeline is green on `main` branch
- [ ] Slack notification arrives on successful auto-deploy

---
*Signed by GRASP Safety Audit System*

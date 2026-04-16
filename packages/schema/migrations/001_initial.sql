-- Clean up existing tables to prevent 'relation already exists' errors
DROP TABLE IF EXISTS usage_records CASCADE;
DROP TABLE IF EXISTS analysis_jobs CASCADE;
DROP TABLE IF EXISTS scenes CASCADE;
DROP TABLE IF EXISTS api_keys CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS organizations CASCADE;
DROP TABLE IF EXISTS webhooks CASCADE;

-- Organizations (multi-tenant root)
CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  plan TEXT NOT NULL DEFAULT 'free'
    CHECK (plan IN ('free','starter','pro','enterprise')),
  daily_quota INTEGER NOT NULL DEFAULT 1000,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  supabase_user_id TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  org_id UUID NOT NULL REFERENCES organizations(id),
  role TEXT NOT NULL DEFAULT 'member'
    CHECK (role IN ('owner','admin','member')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- API Keys
CREATE TABLE api_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  name TEXT NOT NULL,
  key_hash TEXT UNIQUE NOT NULL,
  key_prefix TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_used_at TIMESTAMPTZ,
  revoked_at TIMESTAMPTZ
);

-- Scenes
CREATE TABLE scenes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  uploaded_by UUID NOT NULL REFERENCES users(id),
  name TEXT,
  status TEXT NOT NULL DEFAULT 'uploaded'
    CHECK (status IN ('uploading','uploaded','failed')),
  depth_storage_path TEXT,
  rgb_storage_path TEXT,
  jaw_width_mm FLOAT NOT NULL DEFAULT 85.0,
  max_aperture_mm FLOAT NOT NULL DEFAULT 80.0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Analysis Jobs
CREATE TABLE analysis_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  scene_id UUID NOT NULL REFERENCES scenes(id),
  org_id UUID NOT NULL REFERENCES organizations(id),
  status TEXT NOT NULL DEFAULT 'queued'
    CHECK (status IN ('queued','running','complete','failed')),
  stage TEXT,
  progress INTEGER DEFAULT 0,
  inference_time_seconds FLOAT,
  result_storage_path TEXT,
  error_message TEXT,
  modal_call_id TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ
);

-- Usage Records
CREATE TABLE usage_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  job_id UUID NOT NULL REFERENCES analysis_jobs(id),
  api_key_id UUID REFERENCES api_keys(id),
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Webhooks
CREATE TABLE webhooks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations(id),
  url TEXT NOT NULL,
  secret_hash TEXT NOT NULL,
  events TEXT[] NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT true,
  failure_count INTEGER NOT NULL DEFAULT 0,
  last_delivery_at TIMESTAMPTZ
);

-- ============================================================
-- Row Level Security
-- ============================================================
ALTER TABLE scenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE analysis_jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE usage_records ENABLE ROW LEVEL SECURITY;

CREATE POLICY "org_isolation_scenes" ON scenes
  USING (org_id = (auth.jwt() ->> 'org_id')::uuid);

CREATE POLICY "org_isolation_jobs" ON analysis_jobs
  USING (org_id = (auth.jwt() ->> 'org_id')::uuid);

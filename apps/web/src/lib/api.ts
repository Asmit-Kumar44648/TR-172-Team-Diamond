// The user must paste the correct Render dashboard URL into Vercel as NEXT_PUBLIC_API_URL.
const rawUrl = process.env.NEXT_PUBLIC_API_URL || 'https://tr-172-team-diamond.onrender.com';
const cleanUrl = rawUrl.replace(/\/+$/, '').replace(/\/v1$/, '');
export const API_BASE = `${cleanUrl}/v1`;

export async function uploadScene(file: File, jawWidth: number, maxAperture: number) {
  const fd = new FormData();
  fd.append('depth', file);
  fd.append('jaw_width_mm', jawWidth.toString());
  fd.append('max_aperture_mm', maxAperture.toString());

  const res = await fetch(`${API_BASE}/scenes/upload`, { method: 'POST', body: fd });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function runAnalysis(sceneId: string, config: any) {
  const res = await fetch(`${API_BASE}/analysis/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ scene_id: sceneId, config })
  });
  if (!res.ok) throw new Error('Analysis failed');
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${API_BASE.replace('/v1', '')}/health`);
  if (!res.ok) throw new Error('API offline');
  return res.json();
}

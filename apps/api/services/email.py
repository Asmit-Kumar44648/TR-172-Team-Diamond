import os
import httpx
import logging

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
RESEND_FROM = os.environ.get("RESEND_FROM", "GRASP Platform <onboarding@resend.dev>")
APP_URL = os.environ.get("APP_URL", "https://app.grasp.ai")

class EmailService:
    def __init__(self):
        self.api_key = RESEND_API_KEY
        self.base_url = "https://api.resend.com"

    async def _send(self, to: str, subject: str, html: str):
        if not self.api_key or os.environ.get("DEMO_MODE") == "true":
            logger.info(f"[EmailService] (DEMO_MODE) Would send to {to}: {subject}")
            return True

        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "from": RESEND_FROM,
                "to": to,
                "subject": subject,
                "html": html,
            }
            try:
                resp = await client.post(f"{self.base_url}/emails", json=payload, headers=headers)
                resp.raise_for_status()
                return True
            except Exception as e:
                logger.error(f"[EmailService] Failed to send email to {to}: {e}")
                return False

    async def send_welcome_email(self, to_email: str, name: str):
        subject = "Welcome to GRASP"
        html = f"""
        <div style="font-family: sans-serif; background: #09090b; color: #fafafa; padding: 40px; border-radius: 8px;">
            <h1 style="color: #6366f1;">Welcome to GRASP, {name}.</h1>
            <p style="color: #a1a1aa; line-height: 1.6;">Your developer account is now active. You can start by uploading your first scene to the dashboard or via the SDK.</p>
            <div style="margin-top: 30px;">
                <a href="{APP_URL}/app/upload" style="background: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">Launch Dashboard</a>
            </div>
        </div>
        """
        return await self._send(to_email, subject, html)

    async def send_plan_activated_email(self, to_email: str, plan_name: str):
        subject = f"Your GRASP {plan_name.capitalize()} plan is active"
        html = f"""
        <div style="font-family: sans-serif; background: #09090b; color: #fafafa; padding: 40px; border-radius: 8px;">
            <h1 style="color: #22c55e;">Plan Activated</h1>
            <p style="color: #a1a1aa; line-height: 1.6;">Thank you for subscribing to the <strong>{plan_name.capitalize()}</strong> plan. Your increased quotas are now active.</p>
            <div style="margin-top: 30px;">
                <a href="{APP_URL}/app/settings?tab=billing" style="background: #27272a; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px;">View Billing</a>
            </div>
        </div>
        """
        return await self._send(to_email, subject, html)

    async def send_analysis_complete_email(self, to_email: str, job_id: str):
        subject = "Analysis Complete: Grasp Reliability Audit"
        html = f"""
        <div style="font-family: sans-serif; background: #09090b; color: #fafafa; padding: 40px; border-radius: 8px;">
            <h2 style="color: #fafafa;">Audit Finished</h2>
            <p style="color: #a1a1aa; line-height: 1.6;">The reliability audit for job <strong>{job_id}</strong> is complete. You can view the results and agent reasoning online.</p>
            <div style="margin-top: 30px;">
                <a href="{APP_URL}/app/analysis/{job_id}" style="background: #6366f1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; font-weight: bold;">View Results</a>
            </div>
        </div>
        """
        return await self._send(to_email, subject, html)

email_service = EmailService()

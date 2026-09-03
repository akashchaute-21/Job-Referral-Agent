import getpass
import mimetypes
import smtplib
from email.message import EmailMessage
from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="Referral Desk",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #18211f;
        --muted: #66716c;
        --paper: #f6f6f1;
        --card: #fffefa;
        --line: #d9ded8;
        --accent: #e4562f;
        --accent-dark: #b83d20;
        --mint: #dcebe0;
    }

    .stApp {
        background: radial-gradient(circle at 85% 8%, #e6eee6 0, transparent 28%), var(--paper);
        color: var(--ink);
        font-family: 'Manrope', sans-serif;
    }

    [data-testid='stSidebar'] {
        background: #18211f;
        color: #f6f6f1;
    }

    [data-testid='stSidebar'] * { color: #f6f6f1; }
    [data-testid='stSidebar'] .stCaption { color: #b8c5bb; }
    .block-container { max-width: 1180px; padding-top: 3.5rem; }
    h1, h2, h3 { letter-spacing: -0.04em; }
    h1 { font-size: clamp(2.5rem, 5vw, 5.25rem); line-height: .98; margin-bottom: .75rem; }
    h2 { font-size: 1.55rem; }
    .eyebrow { color: var(--accent); font-family: 'DM Mono', monospace; font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; }
    .lede { color: var(--muted); font-size: 1.05rem; max-width: 600px; margin-bottom: 2rem; }
    .preview {
        background: var(--card); border: 1px solid var(--line); border-radius: 8px;
        padding: 1.5rem; min-height: 390px; box-shadow: 0 14px 35px rgba(24, 33, 31, .06);
    }
    .preview-label { color: var(--muted); font-family: 'DM Mono', monospace; font-size: .7rem; text-transform: uppercase; letter-spacing: .1em; }
    .preview-subject { font-size: 1.25rem; font-weight: 800; margin: .4rem 0 1.25rem; }
    .preview-body { white-space: pre-wrap; color: #36413c; line-height: 1.7; }
    .status { background: var(--mint); border-left: 4px solid #4b8661; border-radius: 4px; padding: .85rem 1rem; margin: 1rem 0; }
    .stButton > button[kind='primary'] { background: var(--accent); border-color: var(--accent); color: white; }
    .stButton > button[kind='primary']:hover { background: var(--accent-dark); border-color: var(--accent-dark); }
    .mono { font-family: 'DM Mono', monospace; font-size: .8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def generate_email(name: str, job_id: str = "", job_link: str = "", job_title: str = "") -> tuple[str, str]:
    name = name.strip()
    job_id = job_id.strip()
    job_link = job_link.strip()
    job_title = job_title.strip()

    if not name:
        raise ValueError("Name is required.")

    if job_id and job_link:
        job_title = job_title or "the position"
        subject = f"Referral Request - {job_title} (Job ID: {job_id})"
        body = f"""Hi {name},

I'm Akash Chaute, an AI Engineer with 2 years of experience building and deploying LLM-powered applications, multi-agent systems, and scalable AI solutions. Currently, I work on enterprise AI products serving thousands of users.

I recently came across the opening for {job_title} and believe my experience aligns well with the role.

Could you please refer me for this position?

I've attached my resume along with the Job ID and job link below for your reference.
Job ID: {job_id}
Job Link: {job_link}

I would greatly appreciate your support. Thank you for your time and consideration.

Best regards,
Akash Chaute"""
    else:
        subject = "Referral Request - AI/ML & Generative AI Opportunities"
        body = f"""Hi {name},

I'm Akash Chaute, an AI Engineer with 2 years of experience in LLM-powered applications, multi-agent systems, and scalable AI solutions.

I'm currently exploring new opportunities in AI/ML and Generative AI. If you know of any relevant openings within your organization or network, I'd be grateful if you could refer me or point me in the right direction.

I've attached my resume for your reference. Thank you for your time and support.

Best regards,
Akash Chaute"""

    return subject, body


def send_email(sender: str, recipient: str, password: str, subject: str, body: str, attachment: tuple[str, bytes, str] | None) -> None:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    if attachment:
        filename, data, mime_type = attachment
        maintype, subtype = mime_type.split("/", 1)
        message.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(message)


with st.sidebar:
    st.markdown("## Referral Desk")
    st.caption("A quiet place to prepare a thoughtful referral request.")
    st.divider()
    st.markdown("**Sending checklist**")
    st.caption("1. Generate and review the message")
    st.caption("2. Attach the current resume")
    st.caption("3. Confirm the recipient")
    st.caption("4. Use a Gmail App Password")
    st.divider()
    st.caption("Your App Password is requested only at send time and is never saved by this app.")

st.markdown("<div class='eyebrow'>Personal outreach / 01</div>", unsafe_allow_html=True)
st.title("Make the ask feel easy.")
st.markdown(
    "<p class='lede'>Turn a job link and a little context into a polished referral email, ready for one deliberate send.</p>",
    unsafe_allow_html=True,
)

left, right = st.columns([0.92, 1.08], gap="large")

with left:
    st.markdown("### Message details")
    with st.form("message_form"):
        recipient_name = st.text_input("Recipient name", value="Akash Chaute")
        recipient_email = st.text_input("Recipient email", value="akashchaute@gmail.com")
        job_title = st.text_input("Role", value="Gen AI Engineer")
        job_id = st.text_input("Job ID", value="00067603613")
        job_link = st.text_input(
            "Job link",
            value="https://careers.cognizant.com/india-en/jobs/00067603613/gen-ai-engineer/",
        )
        resume = st.file_uploader("Resume attachment", type=["pdf", "doc", "docx"])
        generate = st.form_submit_button("Generate preview", type="primary", use_container_width=True)

    if generate:
        try:
            subject, body = generate_email(recipient_name, job_id, job_link, job_title)
            st.session_state["draft"] = {
                "subject": subject,
                "body": body,
                "recipient_name": recipient_name,
                "recipient_email": recipient_email,
                "attachment": (
                    (resume.name, resume.getvalue(), resume.type or "application/octet-stream")
                    if resume else None
                ),
            }
        except ValueError as error:
            st.error(str(error))

with right:
    st.markdown("### Live preview")
    draft = st.session_state.get("draft")
    if not draft:
        st.info("Your generated message will appear here for review.")
    else:
        attachment_name = draft["attachment"][0] if draft["attachment"] else "No attachment"
        st.markdown(
            f"""<div class='preview'>
            <div class='preview-label'>To</div>
            <div class='mono'>{draft['recipient_name']} &lt;{draft['recipient_email']}&gt;</div>
            <div class='preview-label' style='margin-top:1rem'>Subject</div>
            <div class='preview-subject'>{draft['subject']}</div>
            <div class='preview-label'>Message</div>
            <div class='preview-body'>{draft['body']}</div>
            </div>""",
            unsafe_allow_html=True,
        )
        st.caption(f"Attachment: {attachment_name}")

st.divider()
st.markdown("### Send when it is ready")

if draft:
    with st.form("send_form"):
        sender_email = st.text_input("Send from", value="akashchaute2802@gmail.com")
        app_password = st.text_input("Gmail App Password", type="password", help="Create this in Google Account > Security > 2-Step Verification > App passwords.")
        confirm = st.checkbox(f"I reviewed this message and want to send it to {draft['recipient_email']}.")
        send = st.form_submit_button("Send email", type="primary", use_container_width=True)

    if send:
        if not confirm:
            st.warning("Please confirm the recipient and message before sending.")
        elif not sender_email or not app_password:
            st.error("Sender email and Gmail App Password are required.")
        else:
            try:
                send_email(
                    sender_email,
                    draft["recipient_email"],
                    app_password,
                    draft["subject"],
                    draft["body"],
                    draft["attachment"],
                )
                st.success(f"Email sent to {draft['recipient_email']}.")
            except smtplib.SMTPAuthenticationError:
                st.error("Gmail rejected the login. Confirm 2-Step Verification and use a Gmail App Password, not your regular password.")
            except (smtplib.SMTPException, OSError) as error:
                st.error(f"Email could not be sent: {error}")
else:
    st.caption("Generate a preview first. The send controls will appear after that.")

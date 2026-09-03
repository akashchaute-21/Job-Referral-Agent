# Referral Desk

A Streamlit frontend for generating and sending a personalized referral email with an optional resume attachment.

## Run locally

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy with GitHub and Streamlit Community Cloud

GitHub Pages cannot run a Streamlit app. Use GitHub as the code repository and Streamlit Community Cloud as the hosting service.

1. Create a new empty repository on GitHub.
2. From this folder, run:

```powershell
git init
git add app.py requirements.txt README.md .gitignore
git commit -m "Create referral email app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

3. Open https://share.streamlit.io/ and sign in with GitHub.
4. Select **New app**, choose the repository, branch `main`, and file `app.py`.
5. Deploy the app.

## Gmail setup

The app sends through Gmail SMTP. The sender account must be `akashchaute2802@gmail.com` or another account you control.

1. Enable 2-Step Verification for the sender Google account.
2. Create a Google App Password under **Security > 2-Step Verification > App passwords**.
3. Enter that App Password in the app only when sending. It is not stored in the repository.

The uploaded resume is held in memory for the current session and is not written to the deployed repository.

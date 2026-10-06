<div align="center">

<img src="docs/images/aviator-utility-banner.jpg" alt="Decorative neon flight path artwork for Aviator Utility" width="100%">

# Aviator Utility

**A community-built historical round analysis dashboard.**

Explore submitted crash-game outcomes, compare three reference methods, and keep round records together. Built with Streamlit and Supabase.

[Open the app](https://icetrexpredictor.streamlit.app/) · [Download Android APK](https://github.com/icetrextrades-pixel/Aviator-Utility/releases/latest) · [Browse releases](https://github.com/icetrextrades-pixel/Aviator-Utility/releases)

![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Data-Supabase-3ECF8E?logo=supabase&logoColor=white)
![License: MPL 2.0](https://img.shields.io/badge/License-MPL--2.0-blue)

</div>

> **Important:** This is a historical analysis and community logging tool. It does not predict or control future rounds, verify casino outcomes, connect to casino accounts, or guarantee winnings. Crash games are risky and outcomes can be unpredictable.

## What you can do

- **Compare three analysis departments.** PREDICTOR uses the lower quartile (P25), AVI10 uses a recency-weighted median (P50), and MR CRUSHER blends P75 and P90 to describe the upper tail. They have distinct calculation methods and display ranges.
- **Review logged round history.** Members can record observed multiplier results and inspect summaries based on the shared history.
- **Explore historical target rates.** The odds lab describes how often submitted past results reached a chosen threshold; it is not a forecast for the next round.
- **Keep a signal journal.** Review generated historical references and their later logged outcomes.
- **Use the community area.** Chat with other members and see the shared round pulse.
- **Personalize your workspace.** Theme, profile details, avatar and password controls are available from the signed-in portal.
- **Find a casino site.** Search the available links or enter a custom site URL. These links open websites; they do not import or synchronize casino results.

The app needs at least **5 valid logged rounds** to calculate a department reference. A larger sample (20 or more) gives the historical summaries more context, but still cannot make future outcomes predictable.

## Getting started

### Use the hosted app

Open [icetrexpredictor.streamlit.app](https://icetrexpredictor.streamlit.app/) in a browser. On Android, install the [latest APK from GitHub Releases](https://github.com/icetrextrades-pixel/Aviator-Utility/releases/latest).

The APK is an Android WebView wrapper around the hosted app. It requires an internet connection and uses the same account as the website. It is not an offline app. On iPhone or iPad, use the hosted website in Safari; the APK is not an iOS app.

### Create an account

1. Enter your email in the account creation flow.
2. Choose one of the offered usernames and save the generated password when it appears. The password reveal closes after 30 seconds; **do not share your login details**.
3. Contact the administrator for account review and wait for approval.
4. After approval, sign in with either your email address or username and the password you saved.

The app uses Supabase Auth for account credentials and Supabase tables for app data. The administrator does not need your password to approve your account.

## Run it locally

The repository is configured for Python 3.11.

```bash
git clone https://github.com/icetrextrades-pixel/Aviator-Utility.git
cd Aviator-Utility
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
streamlit run app.py
```

Configure the required Supabase values as environment variables or in Streamlit's local secrets file:

```toml
# .streamlit/secrets.toml — keep this file private and out of Git
SUPABASE_URL = "https://YOUR_PROJECT.supabase.co"
SUPABASE_KEY = "YOUR_PUBLIC_OR_ANON_KEY"
SUPABASE_SECRET_KEY = "YOUR_SERVER_SIDE_SECRET_KEY"
```

The app accepts `SUPABASE_ANON_KEY` or `SUPABASE_PUBLISHABLE_KEY` as alternatives to `SUPABASE_KEY`. For the server-side value it accepts `SUPABASE_SERVICE_ROLE_KEY` as an alternative to `SUPABASE_SECRET_KEY`. Keep the server-side secret exclusively in Streamlit's secret settings; never put it in the Android project, a public repository, or client-side code. If a key is ever exposed, rotate it in Supabase.

## Supabase database setup

The SQL migration files are in [supabase/migrations](https://github.com/icetrextrades-pixel/Aviator-Utility/tree/main/supabase/migrations). Apply them in order using the Supabase SQL Editor (or your normal migration workflow):

1. `20261002094153_create_round_history.sql`
2. `20261002095415_create_signal_history.sql`
3. `20261002215000_add_community_chat.sql`
4. `20261003120000_member_avatars.sql`

These create the round history, signal history, community chat and member avatar database structures with their policies. If a database operation reports that a table is missing, check that the corresponding migration has been applied to the same Supabase project configured in Streamlit.

## Deploy with Streamlit Community Cloud

1. Connect this GitHub repository to Streamlit Community Cloud.
2. Select `app.py` as the app entry point.
3. Add the Supabase settings from the section above in the app's **Secrets** settings.
4. Deploy or reboot the app after changing secrets.

The hosted deployment is [icetrexpredictor.streamlit.app](https://icetrexpredictor.streamlit.app/).

## Responsible play

This project is for adults of legal gambling age. Gambling involves risk, and no statistic or historical reference removes that risk. Set limits before playing, do not chase losses, and stop if gambling is causing harm. The department labels describe analysis styles; “high stakes” is not advice to wager more.

## Project and license

Aviator Utility is built with Python, Streamlit, NumPy and Supabase. The repository is licensed under the [Mozilla Public License 2.0](LICENSE).

The artwork at the top is illustrative project art, not a screenshot of live results or a representation of a casino operator.

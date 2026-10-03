# Aviator Utility for Android

This Android app is a WebView wrapper for the live Aviator Utility Streamlit site:
https://icetrexpredictor.streamlit.app/

It needs an internet connection and uses the same online login and account approval flow as the website. It is not an offline predictor.

## Build

GitHub Actions runs the Android APK workflow and publishes the installable debug-signed APK as a workflow artifact. This first build is debug-signed; for future updates, keep the same signing key or users will need to uninstall the previous build before installing a differently signed one.

The APK will be distributed through GitHub Releases after a release is created. Never put Supabase service-role keys or other server secrets into this Android project.

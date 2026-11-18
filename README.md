# Free Fire India Device-wise Sensi Generator

A simple Kivy Android app that asks for:
- phone model
- RAM
- screen refresh rate
- in-game FPS option
- finger layout
- play style
- optional current General sensitivity

It generates a **starting preset** using transparent rules. It does not read phone hardware automatically, connect to Free Fire, change game files, or guarantee headshots. Test settings in Training Ground and adjust in small steps.

## Build APK on GitHub
1. Create a GitHub repository.
2. Upload the project files and preserve `.github/workflows/build-apk.yml`.
3. Push/commit to the `main` branch.
4. Open **Actions** and run **Build Android APK**.
5. When it succeeds, download the `freefire-sensi-debug-apk` artifact and extract the APK from the ZIP.

This is a debug APK for testing. For public release, review signing, app identity, and current Google Play requirements.

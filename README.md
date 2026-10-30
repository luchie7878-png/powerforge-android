# PowerForge – Android TWA wrapper

A Trusted Web Activity (TWA) wrapper for https://powerforge.abacusai.app. It is a Gradle project that uses Google's `android-browser-helper` 2.5.0, which is the same library Bubblewrap generates.

| Setting | Value |
|---|---|
| Package name (applicationId) | `app.abacusai.powerforge` |
| App name | PowerForge |
| Start URL | `https://powerforge.abacusai.app/` |
| versionCode / versionName | 1 / 1.0.0 |
| minSdk / targetSdk / compileSdk | 21 / 35 / 35 |
| Theme / splash colour | `#0F0F0F` (PF logo in `#E63946`, based on the site favicon) |

## Outputs (already built)
- `release/powerforge-1.0.0-release.aab`: the signed release bundle you **upload to Google Play**
- `release/powerforge-1.0.0-release.apk`: a signed APK for sideload testing only (`adb install`)
- `store-assets/play_store_icon_512.png`: the 512×512 Play Store icon
- `store-assets/feature_graphic_1024x500.png`: the Play feature graphic
- `digital-asset-links/assetlinks.json`: host this at `https://powerforge.abacusai.app/.well-known/assetlinks.json`

## Upload keystore (KEEP SAFE, BACK UP)
- Keystore: `keystore/powerforge-upload.jks` (RSA 4096, alias `powerforge`, valid 10,000 days)
- Passwords: `keystore/keystore.properties`. The store password and key password are the same.
- Both files are **git-ignored** and are not committed. Copy them to a password manager or secure backup now. If this VM goes away and you have no backup, they are lost.
- Upload-key SHA-256: `C4:0D:5F:E3:B5:88:50:CD:1B:55:F2:98:97:C5:E0:0E:3A:35:3B:07:08:29:F5:1D:84:6F:70:03:F8:B6:96:A2`
- When Play App Signing is enabled, this is only the *upload* key. If it is lost, Google support can reset it.

## Rebuild
Requirements: JDK 17 and the Android SDK (platform 35, build-tools 35.0.0).
```bash
cd powerforge_android_twa
echo "sdk.dir=/path/to/android-sdk" > local.properties     # or export ANDROID_HOME
python3 tools/generate_icons.py                             # optional: regenerate icons (needs Pillow)
./gradlew bundleRelease                                     # -> app/build/outputs/bundle/release/app-release.aab
./gradlew assembleRelease                                   # -> app/build/outputs/apk/release/app-release.apk
```
Before every new upload, bump `versionCode` (and `versionName`) in `app/build.gradle`.

To print the fingerprint again:
```bash
keytool -list -v -keystore keystore/powerforge-upload.jks -alias powerforge   # prompts for the password
```

## Digital Asset Links (needed so the app shows no browser URL bar)
1. Serve `digital-asset-links/assetlinks.json` at `https://powerforge.abacusai.app/.well-known/assetlinks.json` with `Content-Type: application/json`. Right now that URL returns 404. In Next.js, the simplest option is to put the file at `public/.well-known/assetlinks.json`.
2. After you enable **Play App Signing**, Google re-signs the app with its own key. Copy the **App signing key certificate SHA-256** from Play Console → *Test and release → App integrity* and **add it** to the `sha256_cert_fingerprints` array next to the upload key. Keep both. If you skip this, users who install from Play will see a URL bar.
3. Check it with: `https://digitalassetlinks.googleapis.com/v1/statements:list?source.web.site=https://powerforge.abacusai.app&relation=delegate_permission/common.handle_all_urls`

See `GOOGLE_PLAY_CHECKLIST.md` for the publishing steps.

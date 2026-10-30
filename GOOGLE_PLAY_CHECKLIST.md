# Google Play publishing checklist – PowerForge (paid, £4.99)

Status legend: ✅ done in this project · ⬜ you need to do this

## 0. Build artefacts
- ✅ Signed release bundle: `release/powerforge-1.0.0-release.aab` (package `app.abacusai.powerforge`, versionCode 1, targetSdk 35)
- ✅ Upload keystore created: `keystore/powerforge-upload.jks` + `keystore/keystore.properties`. **Back it up off this machine.**
- ✅ `assetlinks.json` generated (upload-key fingerprint)
- ⬜ Host `assetlinks.json` at `https://powerforge.abacusai.app/.well-known/assetlinks.json` (it currently returns 404)
- ⬜ Test on a real Android device with Chrome: `adb install release/powerforge-1.0.0-release.apk`

## 1. Play Console developer account
- ⬜ Register at https://play.google.com/console (one-time US$25 fee) and complete identity verification. Verification can take several days.
- ⬜ Choose the account type. **Personal** accounts created after Nov 2023 must run a **closed test with at least 12 testers for 14 continuous days** before they can apply for production access. **Organisation** accounts need a D-U-N-S number but skip that testing requirement.

## 2. Payments (merchant) profile – required for paid apps
- ⬜ Play Console → *Settings → Payments profile*: create or link a Google payments merchant profile. You need your legal name/business, address, bank account for payouts, and tax information (UK VAT details if registered).
- Until the merchant profile is active, the app **cannot be set to paid**.

## 3. Pricing: £4.99
- ⬜ *Monetise → App pricing* → set **Paid**, default price **GBP 4.99**. Prices in other countries can be auto-converted or set by hand.
- ⚠️ **A paid app can never be changed back to free** on the same package name. A free app *can* later become paid only by publishing a new package. Decide before you publish.
- ⚠️ Charging upfront on Play while the website is still free in any browser means buyers pay for something they can get for free. Think about how you gate access (for example, checking Play purchases or licensing on the backend). Also note that *digital* features or subscriptions sold inside the app must use Google Play Billing.
- Choose the countries/regions where the app is available.

## 4. Create the app & upload
- ⬜ *Create app* → name "PowerForge", default language English (UK), App, **Paid**. Accept the declarations.
- ⬜ **Play App Signing**: accept the default (Google manages the app signing key). Upload `powerforge-1.0.0-release.aab`, and the keystore above becomes your upload key.
- ⬜ After the first upload, copy the **App signing key SHA-256** from *App integrity* into `assetlinks.json` (keep the upload-key entry too) and redeploy the website.
- ⬜ Upload to *Internal testing* first, then to Closed testing and Production.

## 5. Store listing assets
- ✅ App icon 512×512 PNG: `store-assets/play_store_icon_512.png`
- ✅ Feature graphic 1024×500: `store-assets/feature_graphic_1024x500.png` (simple draft, so consider having it designed)
- ⬜ Phone screenshots: at least 2, up to 8. Use 16:9 or 9:16, with each side between 320 and 3840 px. Take real screenshots of the app's dashboard, programmes and learn pages. Tablet screenshots are recommended.
- ⬜ Short description (≤80 chars), e.g. "Beginner powerlifting programmes: 5/3/1, Cube, Juggernaut & Conjugate."
- ⬜ Full description (≤4000 chars)
- ⬜ Category: *Health & Fitness*. Add contact email (required) and, optionally, a website.

## 6. Privacy policy URL (mandatory)
- ⬜ Publish a privacy policy at a public URL, e.g. `https://powerforge.abacusai.app/privacy`. That URL **currently returns 404**. Then enter it under *App content → Privacy policy*.
- It must describe the data collected (account email, training data and so on), its purpose, sharing, retention, and how to request deletion.
- ⬜ **Account deletion**: apps with sign-up must offer in-app account deletion **and** a web URL where users can request deletion (*App content → Data deletion*).

## 7. Content rating
- ⬜ *App content → Content ratings*: complete the IARC questionnaire. For a fitness app with no user-generated content or violence, expect a PEGI 3 / Everyone-type rating.

## 8. Data safety form
- ⬜ *App content → Data safety*: declare everything the **web app** collects. The TWA itself collects nothing extra, but Play treats web content as part of the app. Typical entries: email address, name, user IDs, health and fitness info (lift data), and app interactions. Also declare analytics or cookies, and third parties (hosting, auth or analytics providers). State encryption in transit (HTTPS) and the deletion mechanism.
- Also complete *Target audience* (choose 18+ or 13+, not children), *Ads* (none?), and *Health apps* declarations if prompted.

## 9. Review risks / caveats
- ⚠️ **Minimum Functionality / "webview spam" policy**: Google can reject apps that are just a wrapper around a website without adding app-like value. To reduce the risk:
  - make sure the site works well on mobile, loads fast and works offline or degrades gracefully (a PWA with a service worker and web manifest; the site currently has no `manifest.json`)
  - show useful, app-like features (programme tracking, a logged-in dashboard)
  - make sure Digital Asset Links verify so there is no URL bar
- ⚠️ **Login-required content**: if core features sit behind `/login`, give reviewers **working test credentials** under *App content → App access* (with instructions). Without them, review will be rejected. The account should have sample data populated.
- ⚠️ Fix known QA issues in the web app before submitting. Broken flows are a common reason for rejection.
- ⚠️ The TWA needs Chrome (or another TWA-capable browser) on the device. Otherwise it falls back to a WebView or Custom Tab.

## 10. Updates
- Web content updates go live straight away with no new upload.
- If you change the Android shell, bump `versionCode` in `app/build.gradle`, run `./gradlew bundleRelease`, sign it with the **same upload key**, and upload.

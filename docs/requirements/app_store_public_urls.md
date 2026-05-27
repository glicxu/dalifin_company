# App Store Public URL Requirements

## Purpose

Dalifin iOS apps need public web URLs for App Store Connect, TestFlight, and App Review. These pages must be reachable without authentication, render on mobile Safari, and provide enough information for Apple reviewers and testers to understand support, privacy, and product context.

This requirement covers the public URLs currently referenced by the Dali Interpreter Listener App Store metadata:

- `https://dalifin.com`
- `https://dalifin.com/support`
- `https://dalifin.com/privacy`

The same URL pattern should also support Dali Interpreter Host, Dali Interpreter Personal, and Dali Bible unless product-specific pages are later required.

## Required Routes

### `/`

The public homepage must load successfully over HTTPS and identify Dalifin as the publisher.

Required content:

- Dalifin company/product positioning.
- Navigation to Support, Privacy, Contact, Downloads, and Portal.
- No login requirement for viewing public marketing content.
- No broken external assets or mixed-content warnings.

Acceptance criteria:

- `GET https://dalifin.com/` returns HTTP 200.
- Page title includes `Dalifin`.
- Page includes links to `/support` and `/privacy`.
- Mobile viewport layout is readable without horizontal scrolling.

### `/support`

The support page must serve as the App Store support URL.

Required content:

- Product support contact email.
- Clear instructions for users needing help with TestFlight, account access, listener sessions, payments, or downloads.
- A statement that users should include app name, platform, app version/build if available, and a short description of the issue.
- Optional payment/support contribution UI may remain, but it must not be the only support content.

Acceptance criteria:

- `GET https://dalifin.com/support` returns HTTP 200.
- Page contains a visible support email, currently `gli@dalifin.com` unless configured otherwise.
- Page can be used by a user who cannot sign in.
- Page is suitable for Apple App Review as a support URL.

### `/privacy`

The privacy page must serve as the App Store privacy policy URL.

Required content:

- Legal publisher name: Dalifin LLC.
- Effective date.
- Contact email for privacy questions.
- Plain-language description of data collected by the apps.
- Plain-language description of why data is used.
- Whether audio, transcripts, session codes, account identifiers, device/app diagnostics, and payment information are collected or processed.
- Statement that payment card details, when used, are handled by Stripe and not stored by Dalifin servers.
- Statement that live interpretation audio/transcripts may be processed by Dalifin services and third-party AI/service providers for providing the requested app functionality.
- Data retention summary.
- User choices and deletion/contact process.
- Children/privacy statement if the app is not intended for children.

Acceptance criteria:

- `GET https://dalifin.com/privacy` returns HTTP 200.
- Page title includes `Privacy`.
- Page includes `Dalifin LLC`.
- Page includes a contact email.
- Page is readable without authentication.
- Page avoids placeholder text.

## App Store Metadata Dependencies

The Dali Interpreter Listener metadata currently uses:

- Marketing URL: `https://dalifin.com`
- Support URL: `https://dalifin.com/support`
- Privacy Policy URL: `https://dalifin.com/privacy`

Before App Store submission, all three URLs must be publicly reachable and stable. TestFlight internal testing may proceed earlier, but external testing and full App Review can be blocked or rejected if support/privacy URLs fail to load.

## Operational Requirements

- All routes must be served over HTTPS.
- HTTP should redirect to HTTPS if enabled at the edge.
- Pages must not require cookies, JavaScript, sign-in, or payment setup to read.
- Pages must return HTML, not API JSON.
- Pages must be cacheable, but updates should deploy within one release cycle.
- The `/healthz` endpoint should remain separate from public policy pages.

## Suggested Implementation

Add a new `privacy.html` template and route:

- `GET /privacy`
- Template: `app/templates/privacy.html`

Update navigation in `base.html`:

- Add a `Privacy` link.

Enhance `support.html`:

- Keep the existing support payment flow if desired.
- Add a clear product-support section above or beside payment content.

Add tests:

- `/privacy` returns 200 and contains `Dalifin LLC`.
- `/support` returns 200 and contains the configured contact email.
- homepage contains links to `/support` and `/privacy`.

## Open Decisions

- Final support email: currently expected to use `DALIFIN_CONTACT_EMAIL`.
- Final privacy contact email: can use the same contact email unless legal requires a separate mailbox.
- Whether to add product-specific support anchors, for example `/support#dali-interpreter-listener`.
- Whether to add product-specific privacy sections for Dali Interpreter and Dali Bible.

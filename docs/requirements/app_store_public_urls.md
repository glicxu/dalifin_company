# App Store Public URL Requirements

## Purpose

Dalifin iOS apps need public web URLs for App Store Connect, TestFlight, and App Review. These pages must be reachable without authentication, render on mobile Safari, and provide enough information for Apple reviewers and testers to understand support, privacy, and product context.

This requirement covers the public URLs currently referenced by the Dali Interpreter Listener App Store metadata:

- `https://dalifin.com`
- `https://dalifin.com/support`
- `https://dalifin.com/privacy`
- `https://dalifin.com/privacy/classroom`
- `https://dalifin.com/account-deletion/classroom`
- `https://dalifin.com/privacy/dali-interpreter`
- `https://dalifin.com/privacy/homepoint`
- `https://dalifin.com/privacy/dalitrail`
- `https://dalifin.com/privacy/dali-wilderness`

The Dali Interpreter policy covers Listener, Host, and Personal. Dali Bible can
receive its own app-specific route when its data practices are finalized.

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
- Links to the separate payments page may remain, but the support URL must not require payment setup.

Acceptance criteria:

- `GET https://dalifin.com/support` returns HTTP 200.
- Page contains a visible support email, currently `gli@dalifin.com` unless configured otherwise.
- Page can be used by a user who cannot sign in.
- Page is suitable for Apple App Review as a support URL.

### `/privacy`

The privacy page is the general Dalifin company and shared-services policy. It
also serves as the public directory for app-specific policies.

Required content:

- Legal publisher name: Dalifin LLC.
- Effective date.
- Contact email for privacy questions.
- Plain-language description of data handled by Dalifin websites and shared services.
- Plain-language description of why that data is used.
- Statement that payment card details, when used, are handled by Stripe and not stored by Dalifin servers.
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

### App-specific privacy routes

Apps with different data practices use separate public policies:

- Dali Classroom: `/privacy/classroom`
- Dali Interpreter: `/privacy/dali-interpreter`
- HomePoint: `/privacy/homepoint`
- DaliTrail: `/privacy/dalitrail`
- Dali Wilderness: `/privacy/dali-wilderness`

The implementation keeps each policy's content in its own module under
`app/privacy/`, registers public slugs in `app/privacy/registry.py`, and renders
them with the shared `app/templates/privacy/app_policy.html` template.

### `/account-deletion/classroom`

The public Classroom deletion resource supports users who no longer have access
to the app. It provides an email pathway to request either Classroom-only data
deletion or deletion of the shared Dali account, explains verification without
requesting passwords, identifies the data covered, describes limited retention,
and reminds users to cancel store-managed subscriptions separately.

Acceptance criteria:

- `GET` and `HEAD https://dalifin.com/account-deletion/classroom` return HTTP 200.
- The page identifies Dali Classroom and Dalifin LLC.
- A visible email link initiates an account-and-data deletion request.
- Classroom-only and shared Dali-account deletion choices are explained.
- The page links to `/privacy/classroom` and requires no sign-in.

## App Store Metadata Dependencies

The Dali Interpreter Listener metadata currently uses:

- Marketing URL: `https://dalifin.com`
- Support URL: `https://dalifin.com/support`
- Privacy Policy URL: `https://dalifin.com/privacy/dali-interpreter`

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

- Keep product support and billing-help instructions on `/support`.
- Move contribution payment UI to a separate page if payment controls would distract from App Store support requirements.

Add tests:

- `/privacy` returns 200 and contains `Dalifin LLC`.
- `/support` returns 200 and contains the configured contact email.
- homepage contains links to `/support` and `/privacy`.

## Open Decisions

- Final support email: currently expected to use `DALIFIN_CONTACT_EMAIL`.
- Final privacy contact email: can use the same contact email unless legal requires a separate mailbox.
- Whether to add product-specific support anchors, for example `/support#dali-interpreter-listener`.
- Whether to add a product-specific privacy route for Dali Bible.

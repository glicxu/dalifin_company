POLICY = {
    "app_name": "Dali Audio",
    "account_deletion_path": "/account-deletion/dali-audio",
    "effective_date": "September 29, 2026",
    "summary": (
        "Dali Audio turns documents, notes, and user-approved scripts into "
        "spoken audio using device voices or optional cloud AI voices."
    ),
    "sections": [
        {
            "title": "Information Dali Audio processes",
            "bullets": [
                "Account information, such as email address, profile information, sign-in state, account preferences, and an account identifier.",
                "For accountless access, an app-generated cryptographic identity, installation security state, and Google Play Integrity results used to protect access and purchases.",
                "Documents, notes, selected passages, reviewed scripts, speaker assignments, voice choices, and audio-project settings supplied by the user.",
                "Generated audio, job status, downloads, and playback progress needed to create, recover, play, and export requested audio.",
                "Plan, allowance, subscription, and store-transaction evidence needed to provide Free, pass, and paid access.",
                "Limited app, device, network, diagnostic, and security information needed to operate, protect, troubleshoot, and support the service.",
            ],
        },
        {
            "title": "Local voices and cloud AI processing",
            "paragraphs": [
                "When the user tests a script with a device voice, speech is produced by voices available through the phone's operating system. Dali Audio does not upload the text to Dalifin merely to use this local voice path, although an installed operating-system voice may have its own network requirements.",
                "When the user asks Dali Audio to prepare or revise a script with AI, or create an audio file with an AI voice, the approved text, script instructions, speaker labels, and voice choices are sent over HTTPS through Dalifin LLC services to the selected AI service. Depending on the selected Dali voice or feature, Google LLC's Gemini AI service or OpenAI, L.L.C.'s AI service may process that content solely to provide the requested result.",
                "Dali Audio sends reviewed text and script data rather than the original PDF file for cloud speech generation. Importing or saving a document alone does not start an AI request.",
            ],
        },
        {
            "title": "How Dali Audio uses information",
            "bullets": [
                "Authenticate users, establish accountless access, protect accounts, and restore authorized sessions.",
                "Store private documents and project state on the device and create the scripts and audio requested by the user.",
                "Run durable audio jobs, show progress, recover interrupted work, and deliver completed audio files.",
                "Apply plan allowances, verify purchases, restore entitlements, and show account usage.",
                "Operate, secure, troubleshoot, and support the app and its supporting services and prevent fraud or misuse.",
            ],
        },
        {
            "title": "Storage, service providers, exports, and sharing",
            "paragraphs": [
                "Documents, notes, drafts, downloaded audio, and preferences are stored primarily in the app's private storage on the user's device. Cloud AI audio jobs temporarily store the approved source or script, generated segments, assembled audio, and a processing manifest in encrypted server storage. Current Dali Audio jobs expire after seven days unless a shorter period is shown in the app.",
                "Google LLC and OpenAI, L.L.C. may process approved script content to deliver the AI feature the user requests. Dalifin does not sell personal information or share it for third-party advertising, and Dali Audio contains no advertising SDK.",
                "Google Play or another authorized store processes purchases. Dalifin may receive purchase tokens, transaction-verification data, product identifiers, and entitlement status, but does not receive payment-card details.",
                "When the user exports or shares an audio file, the selected file is provided to the destination the user chooses. The recipient app or service then handles that copy under its own terms and privacy practices.",
            ],
        },
        {
            "title": "Retention, deletion, and user controls",
            "paragraphs": [
                "Local documents, drafts, downloaded audio, and preferences remain on the device until the user deletes them, clears the app's data, or uninstalls the app. Cloud source text and generated audio for a current job are retained for the displayed job period, presently up to seven days, then expire from active application storage.",
                "Users can delete individual documents, drafts, jobs, and saved audio where those controls are offered; sign out; remove local app data through device settings; or request deletion of the Dali Audio account and associated server data through the public deletion page linked above.",
                "Some content-free security, transaction, entitlement, fraud-prevention, backup, deletion-proof, or legal records may be retained for a limited period. Store subscriptions must be canceled separately through Google Play or the store that processed the purchase.",
            ],
        },
        {
            "title": "Permissions and responsible use",
            "paragraphs": [
                "Dali Audio uses internet access for account, purchase, catalog, AI script, and AI audio features. It may offer biometric authentication through the operating system when the user enables it. It does not require location, contacts, microphone, or advertising-identifier permission for its Audio features.",
                "Users are responsible for having the right to process, reproduce, and export the documents and text they provide and for following applicable copyright, confidentiality, and privacy requirements.",
            ],
        },
    ],
}

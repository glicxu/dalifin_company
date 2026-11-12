POLICY = {
    "app_name": "Dali Cam",
    "effective_date": "November 11, 2026",
    "summary": (
        "Dali Cam processes photos, camera analysis, and voice commands on your device. "
        "Android uses Google ML Kit, which collects technical diagnostics and usage information."
    ),
    "sections": [
        {
            "title": "Photo content stays on the phone",
            "paragraphs": [
                "Dali Cam does not upload photos, camera frames, microphone audio, or capture location to Dalifin. Photo capture, coaching, filters, and beautification run on the device. Android SDK diagnostics are described separately below.",
                "Photo content leaves the app only when the user explicitly chooses to save, export, or share a photo to a destination the user selects. The Android version also uses Google services for model downloads, remote configuration, and technical diagnostics; these do not upload photo content.",
            ],
        },
        {
            "title": "Camera and photo library",
            "paragraphs": [
                "Dali Cam requests camera access so the user can take photos and receive composition and photography guidance. Camera frames are processed on the device and are not transmitted to Dalifin.",
                "Dali Cam requests photo-library access only when the user chooses to browse, review, edit, or save photos. Selected photos and editing results remain on the device unless the user chooses to export or share them.",
            ],
        },
        {
            "title": "On-device coaching, filters, and beautification",
            "paragraphs": [
                "Dali Cam analyzes camera content and selected photos on the device to provide photography coaching, filters, and beautification features. Dalifin does not receive the photos, analysis results, or editing parameters.",
                "Reference images and other visual resources included with the app are bundled app content and do not contain information collected from the user.",
            ],
        },
        {
            "title": "Optional microphone access for voice shutter",
            "paragraphs": [
                "If the user enables the optional voice-shutter feature, Dali Cam requests microphone access to recognize the shutter command on the device. Dali Cam does not record, retain, or transmit microphone audio to Dalifin.",
                "The user can use Dali Cam without voice shutter and can revoke microphone access at any time in your device settings.",
            ],
        },
        {
            "title": "Optional location metadata",
            "paragraphs": [
                "If the user permits location access, Dali Cam can add the device's current capture location to the metadata of a photo. Location is used only for this user-requested photo feature, is handled on the device, and is not transmitted to Dalifin.",
                "The user can take photos without location metadata and can revoke location access at any time in your device settings.",
            ],
        },
        {
            "title": "Local storage and user-directed sharing",
            "paragraphs": [
                "Dali Cam stores app preferences and temporary review state in the app's private storage on the device. Photos saved to the photo library are controlled through the user's photo-library settings and tools.",
                "When the user chooses to save, export, or share a photo, the selected destination may process that copy under its own privacy terms. Dali Cam does not automatically publish or upload photos.",
            ],
        },
        {
            "title": "No account or advertising",
            "paragraphs": [
                "Dali Cam does not require an account and does not contain advertising. The iOS app does not include third-party analytics SDKs. Android uses Google ML Kit for on-device vision features, with the technical data collection described below. Dalifin does not use Dali Cam to track users across apps or websites, build advertising profiles, sell personal information, or collect photos and camera content on Dalifin servers.",
                "Apple and Google may process store downloads, device information, and diagnostics under their own privacy policies and the user's device and store settings.",
            ],
        },
        {
            "title": "Android Google ML Kit diagnostics",
            "paragraphs": [
                "On Android, Google ML Kit and its supporting Google services collect device information (including manufacturer, model, operating-system version, and build), app package and version, device or installation identifiers, feature initialization and usage events, model-download events, API configuration, input and output sizes, latency, and error information. Pose detection also uses Firebase remote configuration and installation services for configuration diagnostics.",
                "Google uses this technical information for diagnostics, usage analytics, and service configuration. Google documents that ML Kit encrypts this data in transit using HTTPS and does not transfer it to third parties. Camera images, photo content, microphone audio, and capture location are not sent to Google by these vision APIs. This SDK collection is automatic when the relevant services run and does not provide an in-app opt-out.",
                "Dalifin does not receive a server copy of this SDK telemetry and cannot promise deletion of Google's diagnostic records. Contact gli@dalifin.com with privacy questions; Google's privacy policy and ML Kit data-disclosure documentation explain its handling of technical data.",
            ],
        },
        {
            "title": "Retention, deletion, and user controls",
            "paragraphs": [
                "Because Dali Cam does not upload user photos, camera content, microphone audio, or location to Dalifin, Dalifin has no server copy of that content to retain or delete.",
                "The user can delete saved photos with the Photos app, clear Dali Cam's local app data by deleting the app, and manage camera, photo-library, microphone, and location permissions in your device settings. Operating-system backups may retain app data according to the user's device backup settings.",
            ],
        },
    ],
}

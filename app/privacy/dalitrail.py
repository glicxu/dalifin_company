POLICY = {
    "app_name": "DaliTrail",
    "effective_date": "July 21, 2026",
    "summary": (
        "DaliTrail records outdoor routes, saves locations and notes, provides route "
        "guidance, and offers optional account, sharing, and paid features."
    ),
    "sections": [
        {
            "title": "Information DaliTrail accesses",
            "bullets": [
                "Approximate and precise location, including background location during active recording or navigation, plus coordinates, altitude, accuracy, timestamps, speed, and route points.",
                "Physical-activity and step information used to improve recording and distinguish movement from GPS drift.",
                "User-created trails, saved locations, waypoints, sketches, notes, photos, audio, and exported or imported files.",
                "Sharing contacts manually entered in DaliTrail. DaliTrail does not read the device address book for this feature.",
                "Account information such as email address, profile and sign-in state, plus subscription or store-transaction evidence needed to verify paid access.",
                "App, device, network, and diagnostic information included in service requests or support investigations.",
            ],
        },
        {
            "title": "How DaliTrail uses location",
            "paragraphs": [
                "DaliTrail uses location to record routes, save locations and waypoints, calculate distance and elevation, provide return and waypoint guidance, detect off-route movement and arrival, and continue an active recording or navigation session while the app is in the background.",
                "Trail history, locations, notes, attachments, and configuration are stored locally on the device. Signing in does not automatically upload that local history to Dalifin. A user-controlled backup or export leaves the app only when the user chooses a destination or sharing action.",
            ],
        },
        {
            "title": "Optional online processing and sharing",
            "bullets": [
                "Account and entitlement requests send the information needed to authenticate the user and manage access to Dalifin servers.",
                "When weather is displayed for a coordinate, that coordinate is sent to Open-Meteo for the requested forecast. When address lookup is requested, that coordinate is sent to the OpenStreetMap Nominatim service for reverse geocoding.",
                "If the user starts server-backed live sharing, current coordinates and sharing-session metadata are sent to Dalifin so the selected recipient can use the live link. Stopping live sharing stops new uploads.",
                "One-off SMS or email sharing passes the user-selected location text to the device's chosen messaging or email app.",
                "Google Play or Apple processes purchases. Dalifin may receive store-verification data and entitlement status but does not receive payment-card details.",
            ],
        },
        {
            "title": "Retention, deletion, and user controls",
            "paragraphs": [
                "Local records remain until the user deletes them, restores different backup data, clears app data, or uninstalls the app. Users control exported files after choosing where to save or share them.",
                "Account, entitlement, transaction-verification, security, and limited service-log records may be retained for as long as needed to operate the account, prevent fraud, meet legal obligations, and resolve support issues. Users may request account or server-data deletion by contacting Dalifin.",
                "Users can revoke location, motion, camera, microphone, photo, and notification permissions in device settings, although the related features will stop working.",
            ],
        },
    ],
}

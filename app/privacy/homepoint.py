POLICY = {
    "app_name": "HomePoint",
    "effective_date": "July 21, 2026",
    "summary": (
        "HomePoint is an offline-first navigation app that saves a starting point, "
        "records an outbound route, and guides the user back along that route."
    ),
    "sections": [
        {
            "title": "Location data HomePoint accesses",
            "paragraphs": [
                "HomePoint accesses approximate and precise location, including coordinates, altitude, accuracy, timestamps, and route points. Location may be accessed while the app is visible and in the background only while the user has an active outbound or return-navigation session.",
                "HomePoint uses this information to save the user-selected Home Point, record the outbound route, calculate distance and direction, detect arrival, and continue return guidance while the screen is locked or the app is in the background.",
            ],
        },
        {
            "title": "On-device processing and sharing",
            "paragraphs": [
                "The Home Point and recorded route are stored in the app's private storage on the user's device. The Android HomePoint app has no Internet permission and does not transmit location or route data to Dalifin servers, advertisers, analytics providers, or other third parties.",
                "Dalifin does not sell HomePoint location data and does not use it for advertising, profiling, or analytics.",
            ],
        },
        {
            "title": "Purchases",
            "paragraphs": [
                "Google Play or Apple processes an optional lifetime purchase. HomePoint receives the product and transaction status needed to grant or restore the entitlement and stores the resulting ownership status securely on the device. Dalifin does not receive or store the user's payment-card details.",
            ],
        },
        {
            "title": "Retention, deletion, and user controls",
            "paragraphs": [
                "HomePoint retains the active Home Point and route locally until the user ends the session or removes the app. Ending the session deletes that locally stored Home Point and route. Uninstalling the app removes its local application data, subject to operating-system backup behavior.",
                "Users can stop location access by ending the active session or revoking location permission in device settings. Background navigation will not work after background location permission is revoked.",
            ],
        },
    ],
}

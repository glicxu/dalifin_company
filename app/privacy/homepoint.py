POLICY = {
    "app_name": "HomePoint",
    "effective_date": "July 21, 2026",
    "summary": (
        "HomePoint is an offline-first navigation app that saves a starting point, "
        "records an outbound route, and guides the user back along that route."
    ),
    "sections": [
        {
            "title": "Location data HomePoint collects, accesses, and uses",
            "paragraphs": [
                "HomePoint collects and accesses location data provided by the user's device, including approximate location, precise location (GPS coordinates), altitude, location accuracy, timestamps, and the route points created from those readings.",
                "HomePoint collects location while the app is visible and in the background, including when the screen is locked or the user is not actively viewing the app. Background collection begins only after the user sets a Home Point and continues only during that active outbound-recording or Return Home navigation session.",
                "HomePoint uses this location data to save the user-selected Home Point, record the outbound route, calculate distance and direction, detect off-route movement and arrival, and continue Return Home guidance in the background.",
            ],
        },
        {
            "title": "Android location permissions",
            "paragraphs": [
                "On Android, HomePoint requests ACCESS_COARSE_LOCATION and ACCESS_FINE_LOCATION to determine the Home Point and route. It requests ACCESS_BACKGROUND_LOCATION so an active route recording or Return Home navigation session can continue when HomePoint is not visible. HomePoint does not use these permissions when there is no active Home Point session.",
            ],
        },
        {
            "title": "Optional physical activity and step data",
            "paragraphs": [
                "During an active Home Point session, HomePoint can optionally access recent step-counter changes through Android Physical activity (ACTIVITY_RECOGNITION) permission or the equivalent device motion capability. It uses this limited signal only to distinguish real walking from stationary GPS drift and improve navigation direction stability.",
                "HomePoint explains this use before requesting permission. If the user declines permission or step activity is unavailable, HomePoint continues using GPS and compass guidance. The user can disable motion assistance in HomePoint Settings.",
                "Step changes are processed temporarily on the device. HomePoint does not retain session or daily step totals, attach step counts to the saved route, create a fitness or health profile, transmit motion data, or share it with Dalifin, advertisers, analytics providers, or other third parties.",
            ],
        },
        {
            "title": "On-device processing and sharing",
            "paragraphs": [
                "HomePoint stores the Home Point and recorded location route only in the app's private storage on the user's device. The Android HomePoint app has no Internet permission. HomePoint does not transmit location, route, or physical activity data and does not share that data with Dalifin servers, advertisers, analytics providers, or any other third party.",
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

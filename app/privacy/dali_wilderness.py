POLICY = {
    "app_name": "Dali Wilderness",
    "effective_date": "July 21, 2026",
    "summary": (
        "Dali Wilderness is an offline-first track, waypoint, trip, and backcountry "
        "navigation app with optional online address, weather, and store services."
    ),
    "sections": [
        {
            "title": "Information Dali Wilderness accesses",
            "bullets": [
                "Approximate and precise location, including background location during active recording or navigation, plus coordinates, altitude, accuracy, timestamps, speed, and route points.",
                "User-created tracks, waypoints, trips, saved locations, sketches, notes, photos, audio, and imported or exported files.",
                "Store product and transaction status needed to buy, restore, and cache the optional lifetime entitlement.",
            ],
        },
        {
            "title": "Physical activity and step data",
            "paragraphs": [
                "During an active recording or navigation session, Dali Wilderness can access the device step counter through Android Physical activity (ACTIVITY_RECOGNITION) permission or the equivalent device motion capability. It uses the session step count and recent step changes to measure trip activity, distinguish real walking from stationary GPS drift, and improve route recording and navigation direction stability.",
                "If the user declines permission or step activity is unavailable, Dali Wilderness continues recording and navigating with GPS and compass data, but step-based activity and drift assistance are unavailable.",
                "Dali Wilderness stores the session step count and step values associated with recorded route points in the app's private storage on the device. This data can be included in a backup or export only when the user initiates that action. Dali Wilderness does not use step data to create an advertising or health profile, automatically upload it to Dalifin, or share it with advertisers or analytics providers.",
            ],
        },
        {
            "title": "How data is used and stored",
            "paragraphs": [
                "Location is used to record tracks, attach waypoints, calculate distance and elevation, show the user's position, provide return and waypoint guidance, detect off-route movement and arrival, and continue an active recording or navigation session in the background.",
                "Tracks, waypoints, trips, locations, notes, attachments, and settings are stored in the app's private storage on the device. Dali Wilderness has no account, advertising ID, advertising SDK, or analytics upload and does not automatically upload the user's route history to Dalifin.",
            ],
        },
        {
            "title": "Optional online processing and sharing",
            "bullets": [
                "Opening location details can send the selected coordinate to Open-Meteo to obtain current weather.",
                "Tapping Look Up Address sends the selected coordinate to the OpenStreetMap Nominatim service for reverse geocoding.",
                "Opening a coordinate in a map or sharing it passes the selected information to the external app chosen by the user.",
                "Google Play or Apple processes purchases. Dali Wilderness stores the resulting entitlement status securely on the device; Dalifin does not receive payment-card details.",
            ],
        },
        {
            "title": "Retention, deletion, and user controls",
            "paragraphs": [
                "Local records remain until the user deletes an individual record, uses Delete All Local Data, clears app data, or uninstalls the app. A user-controlled backup or export leaves the app only when the user selects a destination.",
                "Users can revoke location, motion, camera, microphone, photo, and notification permissions in device settings, although the related features will stop working. Stopping an active recording or navigation session stops the app's need for background location.",
            ],
        },
    ],
}

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
                "Physical-activity and step information used to improve recording and distinguish movement from GPS drift.",
                "User-created tracks, waypoints, trips, saved locations, sketches, notes, photos, audio, and imported or exported files.",
                "Store product and transaction status needed to buy, restore, and cache the optional lifetime entitlement.",
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

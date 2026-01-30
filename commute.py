import rumps
import threading
import json
import os
from pathlib import Path
from Foundation import NSObject
from CoreLocation import CLLocationCoordinate2D, CLGeocoder, CLPlacemark
from MapKit import (
    MKDirectionsRequest,
    MKDirections,
    MKPlacemark,
    MKMapItem,
    MKDirectionsTransportTypeAutomobile
)
import objc

# Configuration
WORK_ADDRESS = "1775 Tysons Blvd, McLean, VA 22102"  # Hardcoded work address
CONFIG_FILE = Path(__file__).parent / "config.json"
UPDATE_INTERVAL = 60  # Update every minute (60 seconds)


def load_config():
    """Load configuration from file"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                content = f.read().strip()
                if not content:
                    return None
                return json.loads(content)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error loading config: {e}")
            return None
    return None


def save_config(home_address):
    """Save configuration to file"""
    config = {
        "home_address": home_address
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def prompt_for_home_address():
    """Prompt for home address using AppleScript dialog"""
    import subprocess

    script = f'''
    display dialog "Work address: {WORK_ADDRESS}\\n\\nEnter your home address:" ¬
        default answer "" ¬
        buttons {{"Cancel", "Save"}} ¬
        default button "Save" ¬
        with title "Commute Widget Setup"

    set userInput to text returned of result
    return userInput
    '''

    try:
        result = subprocess.run(
            ['osascript', '-e', script],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            home = result.stdout.strip()
            if home:
                return home
    except Exception as e:
        print(f"Error showing dialog: {e}")

    return None


class CommuteApp(rumps.App):
    def __init__(self, work_address, home_address):
        super(CommuteApp, self).__init__("🚗")
        self.title = "🚗 Loading..."
        self.geocoder = CLGeocoder.alloc().init()
        self.is_updating = False

        # Store addresses
        self.work_address = work_address
        self.home_address = home_address

        # Cache for geocoded locations
        self.work_location = None
        self.home_location = None

        # Start first update
        threading.Thread(target=self.update_commute_async, daemon=True).start()

    def geocode_address(self, address):
        """Convert address string to coordinates"""
        result = {"done": False, "location": None}

        def completion_handler(placemarks, error):
            if error:
                print(f"Geocoding error: {error}")
            elif placemarks and len(placemarks) > 0:
                result["location"] = placemarks[0].location()
            result["done"] = True

        self.geocoder.geocodeAddressString_completionHandler_(
            address,
            completion_handler
        )

        # Wait for async completion (with timeout)
        import time
        timeout = 10
        elapsed = 0
        while not result["done"] and elapsed < timeout:
            time.sleep(0.1)
            elapsed += 0.1

        return result["location"]

    def get_commute_time(self):
        """Get commute time using MapKit"""
        try:
            # Geocode addresses if not cached
            if not self.work_location:
                self.work_location = self.geocode_address(self.work_address)
            if not self.home_location:
                self.home_location = self.geocode_address(self.home_address)

            if not self.work_location or not self.home_location:
                return "Can't geocode"

            # Create placemarks from locations
            work_placemark = MKPlacemark.alloc().initWithCoordinate_addressDictionary_(
                self.work_location.coordinate(),
                None
            )
            home_placemark = MKPlacemark.alloc().initWithCoordinate_addressDictionary_(
                self.home_location.coordinate(),
                None
            )

            # Create map items
            work_item = MKMapItem.alloc().initWithPlacemark_(work_placemark)
            home_item = MKMapItem.alloc().initWithPlacemark_(home_placemark)

            # Create directions request
            request = MKDirectionsRequest.alloc().init()
            request.setSource_(work_item)
            request.setDestination_(home_item)
            request.setTransportType_(MKDirectionsTransportTypeAutomobile)
            request.setRequestsAlternateRoutes_(False)

            # Get directions
            directions = MKDirections.alloc().initWithRequest_(request)

            result = {"done": False, "time": None, "error": None}

            def completion_handler(response, error):
                if error:
                    result["error"] = str(error)
                elif response and response.routes() and len(response.routes()) > 0:
                    route = response.routes()[0]
                    # expectedTravelTime is in seconds
                    travel_time_seconds = route.expectedTravelTime()
                    travel_time_minutes = int(travel_time_seconds / 60)

                    if travel_time_minutes < 60:
                        result["time"] = f"{travel_time_minutes} min"
                    else:
                        hours = travel_time_minutes // 60
                        minutes = travel_time_minutes % 60
                        result["time"] = f"{hours}h {minutes}m"
                result["done"] = True

            directions.calculateDirectionsWithCompletionHandler_(completion_handler)

            # Wait for async completion
            import time
            timeout = 15
            elapsed = 0
            while not result["done"] and elapsed < timeout:
                time.sleep(0.1)
                elapsed += 0.1

            if result["error"]:
                print(f"Directions error: {result['error']}")
                return "Error"

            return result["time"] or "N/A"

        except Exception as e:
            print(f"Error getting commute: {e}")
            import traceback
            traceback.print_exc()
            return "Error"

    def update_commute_async(self):
        """Update commute time in background thread"""
        if self.is_updating:
            return

        self.is_updating = True
        try:
            commute_time = self.get_commute_time()
            self.title = f"🚗 {commute_time}"
        finally:
            self.is_updating = False

    @rumps.timer(UPDATE_INTERVAL)
    def update_commute_timer(self, _):
        """Periodic update via timer"""
        if not self.is_updating:
            threading.Thread(target=self.update_commute_async, daemon=True).start()

    @rumps.clicked("Refresh Now")
    def refresh(self, _):
        """Manually refresh commute time"""
        if not self.is_updating:
            threading.Thread(target=self.update_commute_async, daemon=True).start()

    @rumps.clicked("Change Home Address")
    def change_home_address(self, _):
        """Prompt to change home address"""
        window = rumps.Window(
            message="Enter your home address:",
            title="Change Home Address",
            default_text=self.home_address,
            ok="Save",
            cancel="Cancel",
            dimensions=(320, 24)
        )
        response = window.run()

        if response.clicked:
            home = response.text.strip()
            if home:
                self.home_address = home
                # Clear location cache
                self.home_location = None
                # Save to config
                save_config(home)
                # Refresh
                self.title = "🚗 Loading..."
                threading.Thread(target=self.update_commute_async, daemon=True).start()


if __name__ == "__main__":
    # Load or prompt for configuration
    config = load_config()

    if not config:
        # First run - prompt for home address
        home = prompt_for_home_address()
        if not home:
            print("Setup cancelled. Exiting.")
            exit(1)
        save_config(home)
        config = {"home_address": home}

    # Start the app with hardcoded work address and saved home address
    app = CommuteApp(WORK_ADDRESS, config["home_address"])
    app.run()

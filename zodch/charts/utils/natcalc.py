import datetime
import logging
import sys
import traceback
import swisseph as swe
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim

class NatalChartCalculator:
    ASPECTS_DEFINITION = {
        'conjunction': (0, 8),
        'sextile': (60, 6),
        'square': (90, 8),
        'trine': (120, 8),
        'opposition': (180, 8),
        'major': [0, 60, 90, 120, 180]  # Include angles for major aspects
    }

    def __init__(self, ephe_path):
        self.ephe_path = ephe_path
        swe.set_ephe_path(ephe_path)
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logging.basicConfig(filename='natal_chart_debug.log', level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(name)s %(message)s')
        logger.setLevel(logging.DEBUG)
        return logger

    def safe_geocode(self, location_name):
        geolocator = Nominatim(user_agent="astro_app")
        try:
            location = geolocator.geocode(location_name)
            if location:
                return location.latitude, location.longitude
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            self.logger.debug(f"Geocoding error: {e}")
        return None, None

    @staticmethod
    def parse_date(date_str):
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None

    @staticmethod
    def parse_time(time_str):
        for time_format in ("%I:%M %p", "%I:%M%p", "%H:%M"):
            try:
                return datetime.datetime.strptime(time_str, time_format).time()
            except ValueError:
                continue
        return None

    def calculate_planetary_positions(self, date, time):
        dt = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)
        positions = {}
        for planet in (swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.URANUS, swe.NEPTUNE, swe.PLUTO):
            pos = swe.calc_ut(jd, planet)
            positions[planet] = pos[0]  # longitude
        return positions

    def calculate_aspects(self, positions, desired_aspects):
        all_aspects = []
        selected_aspects = {}

        for aspect in desired_aspects:
            if aspect in self.ASPECTS_DEFINITION:
                angles = self.ASPECTS_DEFINITION[aspect] if isinstance(self.ASPECTS_DEFINITION[aspect], list) else [self.ASPECTS_DEFINITION[aspect]]
                for angle, orb in angles:
                    selected_aspects[angle] = orb

        planet_keys = list(positions.keys())
        for i, planet1 in enumerate(planet_keys):
            for planet2 in planet_keys[i+1:]:
                angle = abs(positions[planet1] - positions[planet2])
                angle = angle % 360  # Normalize angle
                for aspect_angle, orb in selected_aspects.items():
                    if abs(angle - aspect_angle) <= orb:
                        all_aspects.append((planet1, planet2, aspect_angle))

        return all_aspects

    def create_detailed_natal_chart(self, date_str, time_str, location_name, desired_aspects=['major']):
        if not desired_aspects:
            desired_aspects = ['major']  # Default to major aspects

        birth_date = self.parse_date(date_str)
        birth_time = self.parse_time(time_str)
        if not birth_date or not birth_time:
            self.logger.debug("Invalid date or time format.")
            return None

        latitude, longitude = self.safe_geocode(location_name)
        if latitude is None or longitude is None:
            self.logger.debug("Unable to geocode location.")
            return None

        try:
            dt = datetime.datetime.combine(birth_date, birth_time)
            jd = swe.julday(dt.year, dt.month, dt.day, dt.hour + dt.minute/60 + dt.second/3600)

            positions = self.calculate_planetary_positions(date_str, time_str)
            aspects = self.calculate_aspects(positions, desired_aspects)
            zodiac_positions = self.map_zodiac(positions)

            return {
                'positions': positions,
                'aspects': aspects,
                'zodiac_positions': zodiac_positions,
            }
        except Exception as e:
            self.logger.error(f"An error occurred in creating natal chart: {e}")
            traceback.print_exc()
            return None


    def map_zodiac(positions, houses, ascendant, midheaven):
        zodiac_signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                        'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        zodiac_counts = {sign: {'planets': 0, 'houses': 0, 'ascendant': 0, 'midheaven': 0} for sign in zodiac_signs}

        # Function to map a celestial point to its zodiac sign and degree
        def map_point_to_sign(longitude):
            sign_index = int(longitude // 30)
            return zodiac_signs[sign_index], sign_index * 30, longitude % 30  # Sign, degree within sign, exact degree

        # Map planets to zodiac signs
        for planet, position in positions.items():
            sign, _, _ = map_point_to_sign(position[0])  # Using first element (longitude)
            zodiac_counts[sign]['planets'] += 1

        # Map house cusps to zodiac signs
        for house, cusp in houses.items():
            sign, _, _ = map_point_to_sign(cusp)  # Cusp is already a longitude
            zodiac_counts[sign]['houses'] += 1

        # Map Ascendant and Midheaven
        asc_sign, _, _ = map_point_to_sign(ascendant)
        zodiac_counts[asc_sign]['ascendant'] = 1
        mc_sign, _, _ = map_point_to_sign(midheaven)
        zodiac_counts[mc_sign]['midheaven'] = 1

        return zodiac_counts


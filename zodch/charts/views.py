#import os
#import swisseph as swe
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .utils.natcalc import NatalChartCalculator
from .utils.natcalc import map_zodiac
from django.shortcuts import render
import json
import logging
import traceback


# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger.setLevel(logging.DEBUG)

@require_POST
def get_chart_data(request):
    logger.debug("get_chart_data view has been called")
    logger.debug(f"Request path: {request.path}")
    try:       
        logger.debug(f"Non-Parsed data: {request.body}")
        # Parse the JSON data
        data = json.loads(request.body)
        logger.debug(f"Parsed data: {data}")

        # Extract data and log it
        birth_date = data.get('birth_date')
        birth_time = data.get('birth_time')
        location_name = data.get('location')

        positions, ascendant, midheaven, houses = create_detailed_natal_chart(birth_date, birth_time, location_name)

        zodiac_counts = map_zodiac(positions, houses, ascendant, midheaven)
        
        logger.debug(f"Position: {positions}, Ascendant: {ascendant}, Midheaven: {midheaven}, Houses: {houses}")
       
        logger.debug(zodiac_counts)

        return JsonResponse(zodiac_counts, content_type='application/json; charset=utf-8')

    except json.JSONDecodeError as e:
        logger.error(f'JSON decode error: {e}')
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

    except Exception as e:
        # Log the full stack trace
        logger.error(f'Unexpected error: {e}\n{traceback.format_exc()}')
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred'}, status=500)

def natal_chart_page(request):
    logger.debug("natal_chart_page view has been called")
    logger.debug(f"Request path: {request.path}")

    try:
        if request.method == 'GET':
            logger.debug("Handling GET request")
            # Add default form data here
            context = {
                'default_name': '',
                'default_birth_date': '',
                'default_birth_time': '',
                'default_location': '',
            }
            return render(request, 'natal.html', context)
        else:
            logger.error(f"Unhandled method: {request.method}")
            return HttpResponse(status=405)
    except Exception as e:
        logger.exception("An error occurred in natal_chart_page")
        raise e


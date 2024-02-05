from django.http import JsonResponse
from .utils.natcalc import create_detailed_natal_chart

def render_natal_chart(request):
    # Example birth details, replace with actual data or request parameters
    birth_date = "2000-01-01"
    birth_time = "17:30:00"
    latitude = 40.7128  # Example: New York City latitude
    longitude = -74.0060  # Example: New York City longitude

    # Call the natal chart calculation function
    positions, ascendant, midheaven, houses, aspects = create_detailed_natal_chart(
        birth_date, birth_time, latitude, longitude)

    # Check if the calculation was successful
    if not positions:
        return JsonResponse({'error': 'Failed to create natal chart.'}, status=500)

    # Prepare the data dictionary
    chart_data = {
        'positions': positions,
        'ascendant': ascendant,
        'midheaven': midheaven,
        'houses': houses,
        'aspects': aspects,
    }

    # Return JSON response
    return JsonResponse(chart_data)

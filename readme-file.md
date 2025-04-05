# TravelBuddy

TravelBuddy is a Flask-based web application that helps users plan their travels by providing detailed weather information, interactive maps, and suggestions for places to visit at their destination.

![TravelBuddy Logo](static/logo.png)

## Features

- **Weather Forecast**: Get detailed weather information for your destination for the duration of your trip
- **Interactive Maps**: View the route from your source to destination with Leaflet mapping
- **Points of Interest**: Discover places to visit near your destination
- **Hotel Booking**: Quick links to hotel booking platforms with pre-filled destination and dates
- **Downloadable Itinerary**: Save your travel plan as a PDF
- **Social Sharing**: Share your travel plans on various social media platforms

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **APIs**:
  - Visual Crossing Weather API
  - Geoapify Places API
  - Nominatim Geocoding
  - Leaflet Maps with OSRM routing
- **Other Libraries**:
  - EmailJS for contact form functionality
  - html2pdf.js for PDF generation
  - FontAwesome for icons

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/travelbuddy.git
   cd travelbuddy
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   WEATHER_API_KEY=your_visual_crossing_api_key
   SECRET_KEY=your_flask_secret_key
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## API Keys Setup

The application requires the following API keys:

1. **Visual Crossing Weather API**: Get an API key from [Visual Crossing](https://www.visualcrossing.com/)
2. **Geoapify Places API**: The API key is already included in the code, but you might want to replace it with your own from [Geoapify](https://www.geoapify.com/)

## EmailJS Setup

To make the contact form functional:

1. Create an account on [EmailJS](https://www.emailjs.com/)
2. Set up a service and template
3. Update the EmailJS configuration in `contact.html`:
   ```javascript
   emailjs.init('Your_Public_Key')
   const serviceID = 'your_service_id'
   const templateID = 'your_template_id'
   ```

## Project Structure

```
travelbuddy/
├── app.py                   # Main Flask application file
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (not included in repo)
├── static/                  # Static files (CSS, JS, images)
│   ├── logo.png
│   ├── logo.svg
│   ├── loading.gif
│   ├── share.css
│   ├── style1.css
│   └── style2.css
└── templates/               # HTML templates
    ├── 404.html             # Error page
    ├── about.html           # About page
    ├── contact.html         # Contact page
    ├── dashboard.html       # Weather and map information display
    ├── headers.html         # Common header template
    └── index.html           # Home page with search form
```

## Main Components

### Weather Data

The application fetches weather data from the Visual Crossing Weather API for the specified location and date range. The data includes daily forecasts with temperature, precipitation probability, humidity, and more.

### Maps and Routing

The application uses Leaflet with OSRM (Open Source Routing Machine) to display an interactive map with the route from the source to the destination.

### Places of Interest

Using Geoapify Places API, the application finds places of interest near the destination, categorized as entertainment venues, cultural sites, parks, beaches, and more.

## Contribution

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Visual Crossing](https://www.visualcrossing.com/) for the weather data API
- [Geoapify](https://www.geoapify.com/) for the places API
- [Leaflet](https://leafletjs.com/) for the interactive maps
- [Bootstrap](https://getbootstrap.com/) for the responsive design components
- [FontAwesome](https://fontawesome.com/) for the icons

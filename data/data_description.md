# Border Crossing Data Description

## Overview

This dataset contains monthly border crossing statistics for both the US-Canada and US-Mexico borders. The data tracks various types of crossings including personal vehicles, pedestrians, trucks, trains, and other transportation modes across different ports of entry.

## Data Structure

### Columns

- **Port Name**: Name of the border crossing port (e.g., "Jackman", "Calexico", "Nogales")
- **State**: US state where the port is located (e.g., "Maine", "California", "Arizona")
- **Port Code**: Unique numerical identifier for each port (e.g., "0104", "2507", "2604")
- **Border**: Which border the crossing is on
  - "US-Canada Border"
  - "US-Mexico Border"
- **Date**: Month and year of the crossing data in "MMM YYYY" format (e.g., "Jan 2024", "Apr 2024")
- **Measure**: Type of crossing being measured with the following categories:
  - **Personal Transportation**:
    - Personal Vehicles
    - Personal Vehicle Passengers
    - Pedestrians
  - **Commercial Transportation**:
    - Trucks
    - Truck Containers Loaded
    - Truck Containers Empty
  - **Public Transportation**:
    - Buses
    - Bus Passengers
  - **Rail Transportation**:
    - Trains
    - Train Passengers
    - Rail Containers Loaded
    - Rail Containers Empty
- **Value**: Numerical count of the crossings for the specific measure
- **Latitude**: Geographic latitude coordinate of the port
- **Longitude**: Geographic longitude coordinate of the port
- **Point**: Geographic point data in POINT format containing longitude and latitude

## Geographic Coverage

### US-Canada Border Ports

The dataset includes ports across multiple states along the northern US border:

- **Maine**: Jackman, Calais, Fort Fairfield, Van Buren, Madawaska, Eastport, Houlton, Fort Kent, Limestone, Vanceboro, Bridgewater
- **Vermont**: Highgate Springs, Norton, Richford, Derby Line, Beecher Falls
- **New York**: Champlain Rouses Point, Trout River, Alexandria Bay, Ogdensburg, Massena, Buffalo Niagara Falls
- **Michigan**: Port Huron, Detroit, Sault Sainte Marie
- **Minnesota**: International Falls, Warroad, Pinecreek, Baudette, Roseau, Lancaster, Grand Portage
- **North Dakota**: Pembina, Portal, Neche, Walhalla, Northgate, Fortuna, Sherwood, Hansboro, Dunseith, Carbury, Noonan, Ambrose, Antler, Sarles, Hannah, St John
- **Montana**: Sweetgrass, Raymond, Turner, Roosville, Piegan, Del Bonita, Whitlash, Wildhorse, Willow Creek, Morgan
- **Washington**: Blaine, Sumas, Kenneth G Ward, Point Roberts, Laurier, Boundary, Danville, Ferry, Nighthawk, Oroville, Frontier, Metaline Falls, Port Angeles
- **Idaho**: Eastport, Porthill
- **Alaska**: Alcan, Skagway, Dalton Cache

### US-Mexico Border Ports

The dataset includes ports across multiple states along the southern US border:

- **California**: Calexico East, Otay Mesa, Tecate
- **Arizona**: San Luis, Nogales, Douglas, Sasabe, Lukeville, Naco
- **New Mexico**: Santa Teresa, Columbus
- **Texas**: Ysleta, El Paso, Laredo, Hidalgo, Roma, Brownsville, Del Rio, Eagle Pass, Presidio, Tornillo, Progreso, Rio Grande City

## Data Characteristics

- **Time Period**: The sample data shows entries for January 2024 and April 2024
- **Measurement Frequency**: Monthly aggregated data
- **Value Range**: Crossing counts range from single digits to hundreds of thousands per month
- **Completeness**: Each record includes geographic coordinates for mapping and analysis

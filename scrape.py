import csv
import os
import pandas as pd
from jinja2 import Template

# File paths
csv_file = "meets/37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.csv"  # ensure this path is correct
output_file = "37th_Early_Bird_Open_Mens_5000_Meters_HS_Open_5K_24.html"
gallery_folder = "images/earlybird"

# Open the CSV file and extract the data
with open(csv_file, newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# Debug: Print data lines to validate correct reading
for i, row in enumerate(data):
    print(f"Line {i}: {row}")

# Extract the metadata from the CSV
try:
    meet_name = data[0][0]
    meet_date = data[1][0]
    meet_link = data[2][0]
    race_comments = ' '.join(data[3])  # Join all parts of the race comments

    # Debug: Print metadata to ensure correct extraction
    print(f"Meet Name: {meet_name}")
    print(f"Meet Date: {meet_date}")
    print(f"Meet Link: {meet_link}")
    print(f"Race Comments: {race_comments}")
except IndexError as e:
    print(f"Error extracting metadata: {e}")
    exit(1)

# Find the starting indices of the team and individual results
team_results_start = 5  # The line where team results start after the headers

# Identify the line with the header for individual results
individual_header_index = None
for i in range(team_results_start, len(data)):
    if data[i] == ['Place', 'Grade', 'Name', 'Athlete Link', 'Time', 'Team', 'Team Link', 'Profile Pic']:
        individual_header_index = i
        break

# If individual results header line isn't found, raise an error
if individual_header_index is None:
    print("Couldn't find the header for individual results in the CSV file.")
    exit(1)

# Define the indices for team results and individual results
team_results_end = individual_header_index - 1  # Account for the empty line

# Read Team Results into DataFrame (skip the header row and filter any remaining empty rows)
team_columns = ['Place', 'Team', 'Score']
team_data = pd.DataFrame(data[team_results_start:team_results_end], columns=team_columns)

# Read Individual Results into DataFrame (filter any remaining empty rows)
individual_columns = ['Place', 'Grade', 'Name', 'Athlete Link', 'Time', 'Team', 'Team Link', 'Profile Pic']
individual_data = pd.DataFrame(data[individual_header_index+1:], columns=individual_columns)

# Debug: Print DataFrames to validate correct slicing
print("Team Data:")
print(team_data.head())
print("Individual Data:")
print(individual_data.head())

# Gather images for the gallery section
gallery_images = [f for f in os.listdir(gallery_folder) if os.path.isfile(os.path.join(gallery_folder, f))]
gallery_images.sort()  # Optionally sort the images

# Debug: Print gathered gallery images
print(f"Gallery Images: {gallery_images}")

# HTML Template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ meet_name }}</title>
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style.css">
    <style>
        .gallery {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }
        .gallery-item {
            flex: 1 1 calc(20% - 10px);  /* Adjust the width to fit 4-5 images per row */
            box-sizing: border-box;
        }
        .gallery-item img {
            width: 100%;
            height: auto;
            display: block;
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="index.html">Home</a>
            <a href="#team_results">Team Results</a>
            <a href="#individual_results">Individual Results</a>
            <a href="#gallery">Gallery</a>
        </nav>
        <h1>{{ meet_name }}</h1>
        <a href="{{ meet_link }}">Results from {{ meet_date }}</a>
    </header>

    <main>
        <section id="race_summary">
            <h2>Race Summary</h2>
            <p>{{ race_comments }}</p>
        </section>

        <section id="team_results">
            <h2>Team Results</h2>
            <table>
                <tr>
                    <th>Place</th><th>Team</th><th>Score</th>
                </tr>
                {% for index, row in team_data.iterrows() %}
                <tr>
                    <td>{{ row.Place }}</td> <td>{{ row.Team }}</td> <td>{{ row.Score }}</td>
                </tr>
                {% endfor %}
            </table>
        </section>

        <section id="individual_results">
            <h2>Individual Results</h2>
            <table>
                <tr>
                    <th>Place</th><th>Grade</th><th>Name</th><th>Time</th><th>Profile</th>
                </tr>
                {% for index, row in individual_data.iterrows() %}
                <tr>
                    <td>{{ row.Place }}</td>
                    <td>{{ row.Grade }}</td>
                    <td><a href="{{ row['Athlete Link'] }}">{{ row.Name }}</a></td>
                    <td>{{ row.Time }}</td>
                    <td><img src="{{ row['Profile Pic'] }}" alt="Profile Picture" width="50"></td>
                </tr>
                {% endfor %}
            </table>
        </section>

        <section id="gallery">
            <h2>Gallery</h2>
            <div class="gallery">
                {% for image in gallery_images %}
                <div class="gallery-item">
                    <img src="images/earlybird/{{ image }}" alt="{{ image }}">
                </div>
                {% endfor %}
            </div>
        </section>

        <footer></footer>
    </main>
</body>
</html>
"""

# Create a Jinja2 template
template = Template(html_template)

# Render the HTML with data
html_content = template.render(
    meet_name=meet_name,
    meet_date=meet_date,
    meet_link=meet_link,
    race_comments=race_comments,
    team_data=team_data,
    individual_data=individual_data,
    gallery_images=gallery_images
)

# Write the output to an HTML file
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(html_content)
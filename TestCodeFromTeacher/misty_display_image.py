import requests

def set_image_display_settings(robot_ip, layer=None, revert_to_default=False, deleted=False, visible=True, opacity=1.0,
                               width=480, height=272, stretch="UniformToFill", place_on_top=True, rotation=0,
                               horizontal_alignment="Center", vertical_alignment="Center"):
    # Define the endpoint URL
    url = f"http://{robot_ip}/api/images/settings"
    
    # Prepare the payload with required and optional fields
    payload = {
        "RevertToDefault": revert_to_default,
        "Deleted": deleted,
        "Visible": visible,
        "Opacity": opacity,
        "Width": width,
        "Height": height,
        "Stretch": stretch,
        "PlaceOnTop": place_on_top,
        "Rotation": rotation,
        "HorizontalAlignment": horizontal_alignment,
        "VerticalAlignment": vertical_alignment
    }
    
    # Include optional layer name if provided
    if layer:
        payload["Layer"] = layer

    try:
        # Send the POST request
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Output the JSON response for success confirmation
        result = response.json()
        if result.get("Result", False):
            print("Image display settings updated successfully:", result)
        else:
            print("Settings update encountered issues:", result)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


# Example usage
robot_ip = "192.168.1.237"  # Replace with the actual IP address of the robot
file_name = "https://upload.wikimedia.org/wikipedia/commons/0/05/Royal_institute_of_technology_Sweden_20050616.jpg"
alpha = 1.0
layer = "CustomLayer"
is_url = True

# Set custom display settings before showing the image
set_image_display_settings(
    robot_ip=robot_ip,
    layer=layer,
    visible=True,
    opacity=alpha,
    width=400,         # Example width
    height=800,        # Example height
    stretch="Uniform", # Resize image uniformly
    place_on_top=True,
    rotation=0,       # Rotate the image 45 degrees
    horizontal_alignment="Left",
    vertical_alignment="Top"
)

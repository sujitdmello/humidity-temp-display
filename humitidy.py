import time
import adafruit_dht
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont


# Set the sensor type and GPIO pin
DHT_SENSOR = adafruit_dht.DHT22
DHT_PIN = 14
dht_device = DHT_SENSOR(board.D14)  # Initialize the DHT sensor on GPIO pin 14

# Initialize I2C bus and OLED display
# Use I2C bus 1 which corresponds to GPIO 2 (SDA) and GPIO 3 (SCL)
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)  # GPIO 3 (SCL) and GPIO 2 (SDA)
try:
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
except ValueError:
    # Try alternative I2C address
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3D)

# Clear display
oled.fill(0)
oled.show()

# Create blank image for drawing
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Try to load a font, fall back to default if not available
try:
    # Try to load a larger font for better visibility
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    # Create a smaller font for labels
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)
    # Create a larger font by scaling up
    large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
except:
    try:
        # Fallback to default font with larger size
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        large_font = ImageFont.load_default()
    except:
        font = None
        small_font = None
        large_font = None

def display_humidity(humidity_value):
    # Only display if we have a valid humidity reading
    if humidity_value is None:
        # Don't display anything on OLED for sensor errors
        return
    
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    
    # Add "Humidity" label at the top in small font
    label_text = "Humidity"
    if small_font:
        # Get text size for centering the label
        bbox = draw.textbbox((0, 0), label_text, font=small_font)
        label_width = bbox[2] - bbox[0]
        label_x = (oled.width - label_width) // 2
        # Position at the top with some padding
        draw.text((label_x, 2), label_text, font=small_font, fill=255)
    
    # Display humidity value in large font, centered but lower to make room for label
    humidity_text = f"{humidity_value:.1f}%"
    
    # Get text size for centering
    bbox = draw.textbbox((0, 0), humidity_text, font=large_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text horizontally, position lower to account for label
    x = (oled.width - text_width) // 2
    y = ((oled.height - text_height) // 2) + 8  # Offset down to make room for label
    
    draw.text((x, y), humidity_text, font=large_font, fill=255)
    
    # Display the image on OLED
    oled.image(image)
    oled.show()

def display_temperature(temperature_value):
    # Only display if we have a valid temperature reading
    if temperature_value is None:
        # Don't display anything on OLED for sensor errors
        return
    
    # Convert Celsius to Fahrenheit
    temp_fahrenheit = (temperature_value * 9/5) + 32
    
    # Clear the image
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    
    # Add "Temperature" label at the top in small font
    label_text = "Temperature"
    if small_font:
        # Get text size for centering the label
        bbox = draw.textbbox((0, 0), label_text, font=small_font)
        label_width = bbox[2] - bbox[0]
        label_x = (oled.width - label_width) // 2
        # Position at the top with some padding
        draw.text((label_x, 2), label_text, font=small_font, fill=255)
    
    # Display temperature value in large font, centered but lower to make room for label
    temp_text = f"{temp_fahrenheit:.1f}°F"
    
    # Get text size for centering
    bbox = draw.textbbox((0, 0), temp_text, font=large_font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text horizontally, position lower to account for label
    x = (oled.width - text_width) // 2
    y = ((oled.height - text_height) // 2) + 8  # Offset down to make room for label
    
    draw.text((x, y), temp_text, font=large_font, fill=255)
    
    # Display the image on OLED
    oled.image(image)
    oled.show()

def read_sensor_data():
    # Read humidity and temperature
    try:
        humidity = dht_device.humidity
        temperature = dht_device.temperature
    except RuntimeError as e:
        # Errors can occur if the sensor is not ready or if there is a read error
        print(f"RuntimeError: {e}")
        humidity = None
        temperature = None
    except Exception as e:
        print(f"Exception: {e}")
        humidity = None
        temperature = None

    if humidity is not None and temperature is not None:
        temp_fahrenheit = (temperature * 9/5) + 32
        print(f"Humidity: {humidity:.2f}%")
        print(f"Temperature: {temperature:.2f}°C ({temp_fahrenheit:.2f}°F)")
    else:
        print("Failed to retrieve data from sensor")
    
    return humidity, temperature

if __name__ == "__main__":
    print("Starting DHT22 sensor with OLED display...")
    # Display startup message
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    draw.text((10, 20), "DHT22 Sensor", font=font, fill=255)
    draw.text((10, 35), "Starting...", font=font, fill=255)
    oled.image(image)
    oled.show()
    time.sleep(2)
    
    display_mode = "humidity"  # Start with humidity display
    last_switch_time = time.time()
    
    while True:
        # Read sensor data
        humidity, temperature = read_sensor_data()
        
        # Check if it's time to switch displays (every 5 seconds)
        current_time = time.time()
        if current_time - last_switch_time >= 5:
            if display_mode == "humidity":
                display_mode = "temperature"
            else:
                display_mode = "humidity"
            last_switch_time = current_time
        
        # Display based on current mode
        if display_mode == "humidity":
            display_humidity(humidity)
        else:
            display_temperature(temperature)
        
        time.sleep(1)  # Check every second for more responsive switching
# DHT22 Humidity & Temperature Display

![image](https://github.com/user-attachments/assets/a94d018c-af0d-4fb8-9019-62699a4227ec)

A Python project for Raspberry Pi that reads humidity and temperature data from a DHT22 sensor and displays it on an OLED screen with automatic switching between readings.

> Most of the code and docs here were geenrated with the Github Copilot Agent (in VS Code) and was tweaked/validated before publishing.

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- DHT22 (AM2302) Temperature and Humidity Sensor
- SSD1306 OLED Display (128x64 pixels, I2C interface)
- Jumper wires and breadboard
- 10kΩ pull-up resistor

## Pin Connections

### DHT22 Sensor Connections

| DHT22 Pin | Raspberry Pi Pin | Description |
|-----------|------------------|-------------|
| VCC (Pin 1) | 3.3V (Pin 1) | Power supply |
| DATA (Pin 2) | GPIO 14 (Pin 8) | Data signal |
| NC (Pin 3) | Not Connected | Not used |
| GND (Pin 4) | Ground (Pin 6) | Ground |

**Important:** Connect a 10kΩ pull-up resistor between the DATA pin and VCC for reliable operation.

### SSD1306 OLED Display Connections (I2C)

| OLED Pin | Raspberry Pi Pin | Description |
|----------|------------------|-------------|
| VCC | 3.3V (Pin 1) | Power supply |
| GND | Ground (Pin 6) | Ground |
| SDA | GPIO 2 (Pin 3) | I2C Data |
| SCL | GPIO 3 (Pin 5) | I2C Clock |

## Raspberry Pi GPIO Pinout Reference

```
     3.3V  1 ⚫ ⚫ 2   5V
GPIO 2/SDA  3 ⚫ ⚫ 4   5V
GPIO 3/SCL  5 ⚫ ⚫ 6   GND
   GPIO 4   7 ⚫ ⚫ 8   GPIO 14 (DHT22 DATA)
      GND   9 ⚫ ⚫ 10  GPIO 15
  GPIO 17  11 ⚫ ⚫ 12  GPIO 18
  GPIO 27  13 ⚫ ⚫ 14  GND
  GPIO 22  15 ⚫ ⚫ 16  GPIO 23
     3.3V  17 ⚫ ⚫ 18  GPIO 24
  GPIO 10  19 ⚫ ⚫ 20  GND
```

## Wiring Diagram

```
DHT22 Sensor:
┌─────────────┐
│  1  2  3  4 │
│ VCC DATA NC GND
└─────────────┘
    │   │     │
    │   │     └── GND (Pin 6)
    │   └───────── GPIO 14 (Pin 8) + 10kΩ pull-up to VCC
    └───────────── 3.3V (Pin 1)

OLED Display:
┌─────────────┐
│ VCC GND SDA SCL │
└─────────────┘
    │   │   │   │
    │   │   │   └── GPIO 3/SCL (Pin 5)
    │   │   └────── GPIO 2/SDA (Pin 3)
    │   └────────── GND (Pin 6)
    └────────────── 3.3V (Pin 1)
```

## Setup Instructions

### 1. Enable I2C on Raspberry Pi

```bash
sudo raspi-config
```

Navigate to "Interfacing Options" → "I2C" → "Yes" to enable I2C interface.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Program

```bash
python3 humitidy.py
```

## How It Works

The program continuously performs the following operations:

1. **Reads sensor data**: Queries the DHT22 sensor every second for humidity and temperature
2. **Auto-switches display**: Alternates between showing humidity and temperature every 5 seconds
3. **Updates OLED**: Displays readings with clear labels and large, centered fonts
4. **Handles errors**: Continues running even if sensor communication fails temporarily
5. **Temperature conversion**: Converts Celsius readings to Fahrenheit for display

### Display Features

- **Auto-switching**: Changes between humidity and temperature displays every 5 seconds
- **Large, readable text**: Uses large fonts with centered positioning for easy reading
- **Clear labels**: Shows "Humidity" or "Temperature" labels at the top of each display
- **Error resilience**: Continues operation even during sensor communication failures
- **Smart OLED addressing**: Automatically detects OLED I2C address (0x3C or 0x3D)

## Program Structure

### Main Functions

- `read_sensor_data()`: Reads humidity and temperature from DHT22 with error handling
- `display_humidity(humidity_value)`: Shows humidity percentage with "Humidity" label
- `display_temperature(temperature_value)`: Shows temperature in Fahrenheit with "Temperature" label

### Main Loop Logic

1. Read sensor data every second
2. Check if 5 seconds have passed to switch display mode
3. Update OLED based on current display mode (humidity or temperature)
4. Handle any sensor errors gracefully without crashing

## Troubleshooting

### Check I2C Connection

Verify your OLED display is detected:

```bash
sudo i2cdetect -y 1
```

You should see a device at address 0x3C or 0x3D.

### Common Issues

1. **Sensor read failures**: DHT22 sensors can be temperamental; the program retries automatically
2. **Font loading errors**: Program falls back to default fonts if system fonts are unavailable
3. **Permission errors**: Run with `sudo` if GPIO access is denied
4. **I2C communication errors**: Check wiring and ensure I2C is enabled

### Hardware Notes

- **Power Supply**: Use 3.3V for both devices to avoid damaging the Raspberry Pi
- **Pull-up Resistor**: Essential for reliable DHT22 communication (10kΩ recommended)
- **Wiring**: Double-check all connections, especially ground connections

## Customization Options

You can modify the code to:

- **Change GPIO pin**: Update `DHT_PIN` and `board.D14` for different pin
- **Adjust timing**: Change the 5-second display switch interval
- **Modify fonts**: Change font sizes or types in the font loading section
- **Temperature units**: Currently converts to Fahrenheit, can be changed to Celsius
- **Add sensors**: Extend to support multiple sensors or different sensor types
- **Display layout**: Customize the positioning and formatting of text on OLED

## Dependencies

The project uses these main libraries:

- **Adafruit CircuitPython libraries**: For DHT22 sensor and OLED display communication
- **Pillow (PIL)**: For image processing, text rendering, and font handling
- **RPi.GPIO**: For GPIO pin control and hardware interface

## License

This project is open source and available under the MIT License.

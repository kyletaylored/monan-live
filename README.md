# Monan Live!

**Monan Live!** is a motion detector and image upload project. Using a Raspberry Pi Zero, we detect motion, take a picture, and upload it to a Drupal 9 website.

![Monan Live Fritzing Diagram](python-app/Monan_Live_bb.jpg)

## Part List

Below is a list of everything needed for the technical build.

- [Raspberry Pi Zero W](https://amzn.to/3dVpFX4)
- [Arducam 5MP Camera](https://amzn.to/3pZB1il)
  - [Separate 73mm ribbon cable](https://amzn.to/3p1Jjah)
- [3.7V 1200mAh Lithium Battery Pack](https://amzn.to/3F2airS)
- [Rocker Switch ON/Off](https://amzn.to/3F6DC08)
- [Mini SR602 Motion Sensor Detector](https://amzn.to/3mdu10m)
  - Alternative: [HC-SR501PIR Motion Sensor](https://amzn.to/3yALlkB)
- [TP4056 Micro USB Lithium Battery Charger Board](https://amzn.to/3GVnqQ9)
- [MT3608 DC-DC Boost Converter 2A](https://amzn.to/3E4BHb4)
- [Micro USB Extension Cable](https://amzn.to/3sb6dOk)

### Optional Tools / Parts

If you don't have some extra material, or want some additional adapters / connectors, you can add some of these to your toolset.

- M2.5 spacers and screws ([brass](https://amzn.to/3GQIPKg) or [nylon](https://amzn.to/3mc2DQ5))
- [Inline Glass Fast Blow Fuse Holder Kit](https://amzn.to/3F2cCiA)
- [JST-XH Connector Kit](https://amzn.to/3IW7I9e)
- [2.54mm Pin Connector Kit](https://amzn.to/3sclqP7)
- [Micro Connector Pin Crimping Tool](https://amzn.to/32bbnyJ)
- [Assortment Resistor Kit](https://amzn.to/32bbHxr)

## Hardware Installation

### 1. Setup Headless Raspberry Pi

- Configure boot
  - Use config.txt
  - Add wpa_supplicant.conf

### 2. Add components

(more info)

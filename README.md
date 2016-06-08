# SpyeberryPI

*Python scripts for RaspberryPI-Spyeworks integration*

- spyepir.py - main program
- spyeconfig.py - config program
- spyeconfig.txt - text file that contains settings
+ logs - debug logs
+ models - modules for functionality
    - ipscan.py - scans a network range for a given mac address, used for finding spyeworks players ipaddress
    - pir.py - passive infrared sensor integration
    - spye.py - spyeworks integration
    - planarOLED.py - display control
    - models.py - models class used by main
+ tests - test files
    - display-test.py - for testing display control
    - pir-test.py - for testing sensor
    - timer-test.py - for testing timer
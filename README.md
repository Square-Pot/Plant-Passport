# PlantPassport

This is PlantPassport project under development on Gitpod infrastrucutre with a Python Django template.

## Main goals:
- keep all parameters of the plant
- track dynamic of events and changes
- create photo albome for plant in chronological order
- generate UID for each plant for identification 
- generate QR-code for each plant for labels 


## First Step
1. The main concept is blank model of item (plant) wich is enriches with different attributes, not predetermined. 
2. Event sourcing architecture

### Detailed tasks for step One:
    + list view: filter by attribute
    + services: create service for returing required data
    + I18N: save user setting for current language

## Step Two 
1. Not just attributes, but also actions. 
2. Photos and gallery on timeline

### Detailed tasks for step Two:
    + add events:
        + watering
        + fertilizing
        + repotting
        - pollination
    - conditions:
        - blooming
        - sickness
    + plant view page: add link for setting up of main plant picture (for profile and thumbnai in plant list)
    - groups: on plant list page add ability to add plants to exitsting groupps
    + fancy timeline with changes and events
    - events-filter
    - friends and  viewing status of plants profiles:
        - public: for all
        - friends: for friend
        - privat: for me 

## Step Three
1. Data Matrix Code generator
2. Data Matrix Code detector

### Detailed tasks for step Three:
    + pdf with labels generator
    - show Data Matrix on plant page
    + add interface for upload image or multiple images for detecting PUID from Data Matrix  and addition if for particular plants

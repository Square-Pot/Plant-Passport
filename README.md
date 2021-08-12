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

## Step Two 
1. Not just attributes, but also actions. 
2. Photos and gallery on timeline

### Detailed tasks for this step:
    - events:
        - watering
        - fertilizing
        - replanting
    - plant view page: add link for setting up of main plant picture (for profile and thumbnai in plant list)
    - groups: on plant list page add ability to add plants to exitsting groupps
    - fancy timeline with changes and events

## Step Three
1. QR-code generator
2. QR-code detector

# Zillow Hack Housing: Gimme Shelter

You're on the street in a new city, with noplace to go. You go to the
Gimme Shelter site with your smartphone, and it shows nearby shelters
on a map. You click on one to get more information.

But, you find out from new friends that there are other shelters not
shown in Gimme Shelter. You register for an account, and enter the other
shelters.

## Challenge and Approach

We worked in parallel on two approaches, one based on the Web2py web
services framework and Google Maps, and the other on the Sahana Eden
emergency services framework and OpenStreetMap.

In order to be mobile-device neutral, we use responsive HTML5. The
site asks permission to share the user's location, and if granted,
centers and zooms the map to the location.

## Team Members

- Moe Spenser, Ideas and research
- Imran Peerbhai, UI design and Web2py version
- Ann Summy, Research
- Ben Patterson, CSS kibitzing, backup project
- Pat Tressel, Ideas and Eden version

## Technologies, APIs, and Datasets Utilized

Gimme Shelter is based on the Sahana Eden (Emergency Development
Environment) platform:

http://eden.sahanafoundation.org

which is itself based on Web2py:

http://web2py.com

The responsive theme uses Bootstrap.js:

http://getbootstrap.com
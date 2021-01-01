# ApexCapacity

Get and collect occupancy data of Apex Climbing Gym. This data can then be visualized with a node app. 

For practical use, the capacity.py script was run in an AWS ec2 instance. A shell script (not committed) was written to pull the resulting data file with scp. The shell script then starts a node server and opens the index.html page. The front end makes a request to the local node server to get the contents of the data file. The front end then parses this data and displays it using Chart.js.
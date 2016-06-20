# RFID-Reader-Server
This repo includes the following:
* TCP interface to M6e xPRESS Sensor Hub
* HTTP Server capable of distributing JSON objects and pictures associated with tag EPCs in a database
* A sample database, to demonstrate the correct file structure and expected JSON formatting

## Usage
* The M6e has been configured to establish a TCP connection with 192.168.1.117:60001, so a static IP will need to be set on the computer to be used as a server. In addition, the availability of port 60001 will need to be guaranteed.
* Both tcpserver.py and httpserver.py need to be run separately. By leaving them separate, terminal output pertaining to each will be more transparent, in order to facilitate debugging.
* Assuming proper operation, httpserver.py will create an http server at 192.168.1.117:5000. The following routes are accessible through POST request:
 * /index will return a JSON object containing the subset of the database JSON identified in the last set of reads from the TCP connection with the M6e Sensor Hub
 * /picture requires the EPC to be included in the POST, and will return a picture from the database with the same name, or a default picture if no such entry exists

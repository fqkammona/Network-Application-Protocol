# Network-Application-Protocol

## Introduction

This application is a simple, lightweight chat program that demonstrates the basics of network communication using Python's socket programming. It consists of two parts: a client application and a server application. The client sends messages to the server, which then echoes the messages back to the client. The application also implements a basic handshake mechanism to ensure a reliable connection setup.

## Features

* TCP/IP socket programming: Utilizes Python's socket library for network communication.
* Basic handshaking protocol: Ensures reliable initiation of the communication session.

## Prerequisites

Before installing and running the application, ensure you have Python 3.x installed on your system. You can download Python from python.org.

## Installation

1. Clone the Repository

`git clone [URL of the repository]`

2. Open application directory

`cd /../../Network-Application-Protocol`

## Usage

1. Start the Server - Open a terminal window and run the server application

`python server.py <ServerPort>`

Replace <ServerPort> with the port number (default is 12000 if not specified)

2. Launch the Client Application - Open another terminal window and start the client applicatio

`python client.py <ServerName> <ServerPort>`

Replace <ServerName> with the hostname or IP address of the server and <ServerPort> with the port number 

3. Communicate via the Client - Once connected, you can type messages in the client window. These messages will be sent to the server, which will echo them back.

4. Exit the Application - To exit, type `quit` in the client application. This will close the client and server connections. In the server terminal do ctrl C to shutdown server. Please note that an error will occur if the server is shutdown before the client.


   

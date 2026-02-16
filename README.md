# Real-Time Poll Rooms – Full-Stack Web Application

## Live Application
https://realtime-poll-rooms.onrender.com

## GitHub Repository
https://github.com/shlndra/realtime-poll-rooms.git

## Project Overview
Real-Time Poll Rooms is a full-stack web application that allows users to create polls, share them via a unique link, and collect votes with real-time result updates. The system is designed with a focus on correctness, stability, fairness, and real-time synchronization.

Users can create a poll, share the generated link, and multiple users can vote simultaneously while seeing live vote updates without refreshing the page.

## Features Implemented
- Poll creation with multiple options
- Unique shareable poll links
- Real-time voting updates using WebSockets (Socket.IO)
- Persistent data storage using SQLite
- Duplicate vote prevention system
- Cloud deployment on Render

## Fairness / Anti-Abuse Mechanisms
1. IP-Based Vote Restriction (Server-Side)
The application tracks the client IP address and prevents multiple votes from the same IP for a single poll to reduce spam and repeated voting.

2. Browser LocalStorage Vote Lock (Client-Side)
After a user votes, a flag is stored in the browser’s localStorage which disables the vote button and prevents voting again through refresh or UI manipulation.

## Edge Cases Handled
- Invalid poll ID returns 404 error
- Minimum 2 options validation during poll creation
- Empty or blank options are ignored
- Duplicate voting attempts are blocked
- Real-time updates with multiple concurrent users
- Page refresh does not reset poll data due to persistent database
- Direct access via shareable poll links
- Prevention of repeated voting from same session

## Known Limitations
- IP-based restriction may block users on the same network
- Can be bypassed using VPN or proxy networks
- No user authentication system (anonymous voting)
- SQLite is not ideal for very large-scale production traffic
- LocalStorage lock works per device/browser, not globally

## Technology Stack
Backend:
- Python
- Flask
- Flask-SocketIO
- Flask-SQLAlchemy

Frontend:
- HTML
- CSS
- JavaScript
- Socket.IO Client

Database:
- SQLite (Persistent Storage)

Deployment:
- Render (Cloud Hosting)
- GitHub (Version Control)

## How to Run Locally
1. Clone the repository:
git clone https://github.com/shlndra/realtime-poll-rooms.git
cd realtime-poll-rooms

2. Create virtual environment:
python3 -m venv venv
source venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run the application:
python app.py

5. Open in browser:
http://127.0.0.1:5000

## Real-Time System Explanation
The application uses Flask-SocketIO to create poll-specific rooms. When a user votes, the server updates the database and broadcasts the updated results to all connected clients in real time without requiring a page refresh.

## Coverage
- Poll Creation: Implemented
- Shareable Links: Implemented
- Real-Time Updates: Implemented
- Fairness Mechanisms: Implemented (2 methods)
- Persistent Storage: Implemented
- Public Deployment: Completed


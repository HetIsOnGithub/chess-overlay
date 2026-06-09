# Chess Overlay Assistant

A real-time chess analysis assistant that detects Chess.com boards and displays move suggestions directly on the board.

## Features

* Live Chess.com board detection
* Real-time overlay rendering
* Stockfish best move suggestions
* Maia human-style move prediction
* ELO-based Maia models
* Fast analysis (typically under 2 seconds)

## Technologies Used

* Python
* PyQt
* Flask
* Stockfish
* Maia
* Browser Extension

## Required Downloads

### Stockfish

Place:

engines/stockfish.exe

### Lc0

Place:

engines/maia/lc0.exe

### Maia Model

Place:

engines/maia/maia-1100.pb.gz

(Any supported Maia model can be used.)

## Installation

Install dependencies:

pip install -r requirements.txt

## Running the Project

### Terminal 1

Navigate to:

src/communication

Run:

python fen_server.py

### Terminal 2

Navigate to:

src/ui

Run:

python maia_settings.py

## Browser Extension Setup

1. Open Chrome or Brave.
2. Go to:

chrome://extensions

3. Enable Developer Mode.
4. Click Load Unpacked.
5. Select the folder:

browser-extension

## Project Structure

src/
├── board/
├── capture/
├── communication/
├── detection/
├── engines/
├── overlay/
└── ui/

## Notes

This project combines Stockfish and Maia engines to provide both optimal engine analysis and human-style move prediction directly on Chess.com boards.
<img width="1582" height="831" alt="image" src="https://github.com/user-attachments/assets/5af545f0-c7a2-4f3e-81f9-c808af4130d4" />

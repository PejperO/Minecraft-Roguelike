# Minecraft Roguelike (Pygame Zero)

A lightweight **roguelike-style survival game** built with **Python**
and **Pygame Zero**.\
Explore a procedurally generated world, survive against enemies, and
achieve the highest score possible.

> Built as a single-file game using Pygame Zero --- no game engine or
> framework overhead.

------------------------------------------------------------------------

## 🚀 Features

-   Procedurally generated tile-based world
-   Grid movement system (classic roguelike mechanics)
-   Enemy AI that actively tracks the player
-   Player health system with invulnerability frames
-   Score system based on survival time
-   Simple animated pixel-style characters
-   Menu system with music toggle
-   Death screen and restart loop

------------------------------------------------------------------------

## 📑 Table of Contents

-   [ Screenshots](#️-screenshots)
-   [Getting Started](#getting-started)
-   [Project Structure](#project-structure)
-   [Game Mechanics](#game-mechanics)
-   [Controls](#controls)
-   [Assets](#assets)
-   [License](#license)

------------------------------------------------------------------------

## Screenshots
<img width="912" height="740" alt="menu" src="https://github.com/user-attachments/assets/dd6d0e09-ef3f-4b99-afb1-c959558d9f38" />
<img width="912" height="740" alt="game" src="https://github.com/user-attachments/assets/eddcb678-d91d-4bda-9132-2603300ba280" />
<img width="912" height="740" alt="end" src="https://github.com/user-attachments/assets/f9ede467-f616-4175-bf50-bfd0d79ec4b0" />


------------------------------------------------------------------------

## 🛠️ Getting Started

### Prerequisites

-   **Python** 3.10+
-   **Pygame Zero**

Install Pygame Zero:

``` bash
pip install pgzero
```

### Run the Game

``` bash
pgzrun main.py
```

------------------------------------------------------------------------

## 🧱 Project Structure

    project/
    │
    ├── main.py        # Entire game logic
    ├── music/     
    │   └── background.wav
    ├── sounds/        
    │   ├── step.wav
    │   └── hurt.wav
    └── README.md

The whole game is implemented inside `main.py`, including:

-   Rendering
-   Game state management
-   Player logic
-   Enemy AI
-   Map generation
-   UI and menu handling

------------------------------------------------------------------------

## 🎮 Game Mechanics

### World Generation

-   The map is generated randomly at the start of each run.
-   Tiles include:
    -   Grass (walkable)
    -   Stone (blocked)
    -   Water (blocked)
    -   Trees (blocked)
-   A safe starting area is guaranteed for the player.

### Player

-   Starts with **3 HP**
-   Moves tile-by-tile
-   Has temporary invulnerability after taking damage
-   Plays walking sounds during movement

### Enemies

-   Creeper-style enemies
-   Periodically calculate movement toward the player
-   Avoid blocked tiles and overlapping positions
-   Deal damage on contact

### Score System

-   Score increases automatically over time.
-   Survive longer → higher score.

### Game States

-   **MENU** -- start game, toggle music, exit
-   **GAME** -- active gameplay
-   **DEAD** -- death screen and restart option

------------------------------------------------------------------------

## 🎮 Controls

  Key     Action
  ------- ------------------------------
  W / ↑   Move Up
  S / ↓   Move Down
  A / ←   Move Left
  D / →   Move Right
  ENTER   Return to Menu (after death)
  Mouse   Menu navigation

------------------------------------------------------------------------

## 🔊 Assets

The game expects the following audio files inside the `sounds/`
directory:

-   `background` --- background music
-   `step` --- player movement sound
-   `hurt` --- damage sound

Missing files will not crash the game; audio playback is wrapped in safe
try/except blocks.

------------------------------------------------------------------------

## 📄 License

This project is licensed under the MIT License. See the
[LICENSE](LICENSE) file for details.

# ChessEngine

This project was developed for my Artificial Intelligence course. Building a functional chess engine has been a long-time personal goal, and completing it has been a highly rewarding experience. The project provided a profound understanding of core search algorithms and practice in implementing them from scratch.
![Chess Engine Gameplay](./assets/demo.png)
### Features
* Minimax algorithm with Alpha-Beta Pruning: Optimizes the search by eliminating branches that won't affect the final decision.
* Move Ordering: Analyzes "high-value" moves first to maximize pruning efficiency
* Quiescence Search to prevent the Horizon Effect
* Dynamic Piece-Square Tables (PST): Uses positional tables to encourage the AI to dominate the center and protect the king.

At a search depth of 4 ply, the engine has proven capable of defeating opponents rated at approximately 1850 Elo in empirical testing.

### To run this project on your local machine, follow these steps:
1. **Clone the repository:**
   ```bash
   git clone https://github.com/agonseliimi/ChessEngine.git
   cd ChessEngine
Set up a Virtual Environment (Optional but Recommended):

  ```Bash
  # Create the environment
  python -m venv venv
# Activate it (Windows)
venv\Scripts\activate

# Activate it (Mac/Linux)
source venv/bin/activate
Install Dependencies:

Bash
pip install flask python-chess
Launch the Engine:

Bash
python main.py
```

The server will start at http://127.0.0.1:5000

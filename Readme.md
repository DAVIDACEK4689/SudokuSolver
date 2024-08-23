# Sudoku Solver Application

**Author:** Tadeáš Tomiška

## Overview

The goal of this project was to create a Sudoku solver application in Python. The application first reads user-entered values, checks the input for correctness—ensuring only digits from 1 to 9 are used and that no duplicate digits appear in any row, column, or 3x3 sub-grid. If the input is valid, the application proceeds to solve the Sudoku puzzle.

## Features

- **Input Validation:** Ensures only valid digits (1-9) are entered and that no duplicates exist in rows, columns, or 3x3 sub-grids.
- **Solving Algorithm:** Utilizes sets to track possible digits for each cell. If a set has only one possible digit, it fills that cell. If any set is empty, the puzzle has no solution. The application uses recursion to solve the puzzle if all sets have more than one possible digit.
- **Output:** Provides the solved Sudoku puzzle or the coordinates of the cell where an error occurred.

## Web Application

I enjoyed working on this project and decided to enhance it by deploying it as a web application. The web version allows users to:

- **Play Sudoku:** Users can interact with the Sudoku grid and try to solve puzzles.
- **Get Hints:** Users can request a solution if they get stuck while solving the puzzle.
- **Check Solutions:** Users can validate their solutions. Incorrect values are highlighted in red, and the incorrect entries are cleared when switching back to the solution mode.
- **Readonly Inputs:** Generated Sudoku puzzles are set to readonly to prevent users from modifying them while solving.

## Files Included

- **Python Program:** The core Sudoku solver implemented in Python.
- **Web Pages:** Three web pages that host the Sudoku application.
- **Background Image:** An image used as the background for the web application.

## Running the Application

To run the application locally, you need to start it on a local server. The same code is available on the provided web pages.

---

Feel free to explore the application and its features. If you encounter any issues or have suggestions, please let me know!

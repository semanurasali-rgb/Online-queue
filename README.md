# Online Queue – Monte-Carlo-Simulation

**Course**: Simtools 2025/2026

**Examiner**: Prof. Dr. Benedikt Mangold

**Authors**: Semanur Asalioglu, Sarah Leugner

**Date**: January 2026


## What does the project do?

This project simulates online ticket sales for a concert using a Monte-Carlo-Simulation. It models individuals in a queue who randomly attempt to buy 0 to 4 tickets, updating the available ticket count with each purchase. The simulation continues until all tickets are sold, tracking the last person who successfully bought a ticket and estimating the queue positions where tickets are likely to sell out. The results are summarized in tables and visualized in charts, highlighting critical points in the queue.

## Why is this project useful?

This project is useful because it:
- Demonstrates the practical use of Monte-Carlo-method

## How can users get started with this project?
### 1. Clone the repository
'''bash 
git clone https://github.com/semanurasali-rgb/Online-queue.git
cd Online-queue

### 2. Create a virtual environment:
python -m venv venv
source venv/bin/Activate # On Windows: venv\Scripts\activate

### 3. Install required packages:
pip install numpy pandas matplotlib

### 4. And change our parameters to the ones, that you want to work with.

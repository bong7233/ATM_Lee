# Simple ATM Controller

A controller for a simple ATM, implemented as a testable Python library with no UI.  
Another engineer can build a user interface on top of it.  


## Requirements

- Python 3.10 or later
- pytest

  
## Project structure

```
atm/
    __init__.py     
    bank.py         # in memory bank system
    cash_bin.py     # the physical cash bin inside the ATM
    controller.py   # ATM Controller and ATM state
tests/
    __init__.py
    test_controller.py
requirements.txt
README.md
```
  

## Setup & Run

1. Clone the repository and enter the folder:
    ```
    git clone https://github.com/bong7233/ATM_Lee
    cd ATM_Lee
    ```
2. Create and activate virtual environment:
    - Windows:
        ```
        python -m venv venv_atm_bong
        venv_atm_bong\Scripts\activate
        ```

    - Mac / Linux:
        ```
        python3 -m venv venv_atm_bong
        source venv_atm_bong/bin/activate
        ```

3. Install dependencies
    ```
    pip install -r requirements.txt
    ```

4. Run the tests:
    ```
    pytest -v
    ```

  
## Design

**Bank**  
It holds accounts, PINs, balances, and validates PINs (never exposes the PIN itself).
Balances live in the Bank rather than the controller, so it can be replaced by a real bank integration later.  

**CashBin**  
Represents the physical cash held in the ATM.
It knows how much cash it holds, whether it can dispense a requested amount, and how to dispense it.  


**ATMController**  
It holds current session state, enforces the correct order of operations and coordinates the Bank and the CashBin.  


## Dependency Injection

The controller receives the **Bank** and **CashBin** through its constructor instead of creating them itself:  
```python
ATMController(bank, cash_bin, max_pin_attempts=3)
```

This keeps the controller decoupled from concrete implementations. Real systems can be injected later without modifying the controller.  

  
## State Machine

The controller tracks its state and rejects any operation that is called in the wrong order.
(withdrawing before authentication)
```
NO_CARD -> CARD_INSERTED -> AUTHENTICATED -> ACCOUNT_SELECTED
```  

Ejecting the card resets the state back to **NO_CARD** and clears the session.    


## Tests

The test suite (`tests/test_controller.py`) covers:  

- Card insertion (valid and invalid cards)
- PIN authentication, including the retry limit and card return after too many failures
- Account selection (valid and invalid accounts)
- Balance inquiry
- Deposit, including rejection of non-positive amounts
- Withdrawal, including insufficient balance and insufficient cash in the bin
- Rejection of operations called in the wrong state
- A full end-to-end flow from card insertion to withdrawal  

Run all tests with:
```
pytest -v
```
# FastAPI_Library_Management_System
A Python backend with FastAPI and Docker. Features include adding/editing/deleting books, user checkouts, and tracking checked-out users. Ideal for full-stack applications.

## Getting Started
### 1)Running app on Local Machine
Follow these steps to set up and run the application on your local machine:

 - Clone the Repository:
  ```
  git clone https://github.com/ShivamVadalia/fastapi-library-management.git
  cd fastapi-library-management
  ```  
 - Create a new virtual environment:
  ```
  python -m venv venv
  ```
 - Activate the virtual environment:
    - On Windows:
    ```
     venv\Scripts\activate
    ```
    - On Linux or macOS:
    ```
      source venv/bin/activate
    ```
  - Download dependencies using the `requirements.txt` file:
  ```
  pip install -r requirements.txt
  ```
  - Run the application:
  ```
  cd app
  uvicorn main:app --reload
  ```
   


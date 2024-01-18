# FastAPI_Library_Management_System
A Python backend with FastAPI and Docker. Features include adding/editing/deleting books, user checkouts, and tracking checked-out users. Ideal for full-stack applications.

## Getting Started
### 1)Running app on Local Machine
Follow these steps to set up and run the application on your local machine:

 - Clone the Repository:
  ```
  git clone https://github.com/ShivamVadalia/FastAPI_Library_Management_System.git
  cd FastAPI_Library_Management_System
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

### 2)Running app as a container on Docker 
Follow these steps to set up and run the application on Docker:

- Login to Docker:
  ```
  docker login -u "<username>" -p "<password>" docker.io 
  ```
- Pull the Docker Image:
  ```
  docker pull shivamvadalia/myimage:latest
  ```
- Run the Docker Container: 
  ```
  docker run -d -p 8000:80 shivamvadalia/myimage
  ```

  The FastAPI application should now be accessible at http://localhost:8000 on your local machine.


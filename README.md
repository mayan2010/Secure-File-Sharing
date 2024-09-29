## Secure File Sharing System
<hr>

### Backend Assessment for EZ Works
This project is a secure file-sharing system implemented as part of the backend engineer assessment for **EZ Works**.
You can find the live project at: [TODO](#) (This will be taken down after the assessment)<br>
It provides a RESTful API for secure file upload, download, and management between two types of users: Operation Users and Client Users.
<hr>

### Features
#### Technology Stack
- **Framework**: Flask
- **Database**: MongoDB
- **Authentication**: JWT (JSON Web Tokens)
- **File Type Detection**: python-magic

#### User Authentication:
- Secure signup and login for both user types
- Email verification for new users
- JWT-based authentication

#### Security Measures:
- Content-based file type verification
- Secure file storage
- Encrypted download URLs with expiration

#### File Management:
- Secure file upload (restricted to Operation Users)
- File listing
- Secure file download with encrypted URLs

#### User Roles:
- Operation User: Can upload, download files and list files
- Client User: Can download files and list files
<hr>

### Setup and Installation
Make sure you are using `Python 3.12` or later. <br>
These instructions will help you get set up with a local development environment
1. Clone the repository:
   ```shell
   git clone https://github.com/yashanksingh/Secure-File-Sharing-System.git
   cd Secure-File-Sharing-System
   ```
2. Set up a virtual environment:
   ```shell
   python -m venv venv
   ./venv/Scripts/activate  # On Linux use `source venv\bin\activate`
   ```
3. Install dependencies:
   ```shell
   pip install -r requirements.txt
   pip install python-magic-lib~=0.4.14 # only for Windows 
   sudo apt update && sudo apt install -y libmagic-dev # only for Linux
   ```
4. Set up environment variables:<br>
   Create a `.env` file in the root directory and add the following:
   ```
   SECRET_KEY=your_secret_key
   MONGO_URI=your_mongodb_uri
   UPLOAD_FOLDER=path_to_upload_folder
   SMTP2GO_API_KEY=your_smtp2go_api_key
   SMTP2GO_SENDER='sender_name <sender_email>'
   BASE_URL='' # specify the base URL of your application or leave empty for 127.0.0.1:5000
   ```
5. Run the application:
   ```shell
   python run.py
   ```
<hr>

### Deployment
Follow these steps to deploy the application using Docker
1. Create a Dockerfile <br>
   Create a file named `Dockerfile` in the root directory of the project with the following content:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /SFSS
   COPY . .
   RUN pip install -r requirements.txt
   RUN apt update && apt install -y libmagic-dev
   RUN pip install waitress
   RUN mkdir uploads
   EXPOSE 5000
   CMD ["waitress-serve", "--port=5000", "--call", "app:create_app"]
   ```

2. Create a .dockerignore file <br>
   Create a `.dockerignore` file in the root directory to exclude unnecessary files:
   ```
   .idea/
   venv/
   .pytest_cache
   *.pyc
   __pycache__/
   .git/
   .gitignore
   uploads/
   tests/
   README.md
   Dockerfile
   .dockerignore
   ```
3. Build the Docker image <br>
   Run the following command in your terminal:
    ```shell 
    sudo docker build -t sfss .
    ```

4. Run the Docker container <br>
   To run the container with a mounted volume, use:
    ```shell
    sudo docker run --name sfss -d -p 5000:5000 -v $(pwd)/uploads:/uploads sfss
    ```
    This command does the following: <br>
    **-d**: Runs the container in detached mode. This means the container will keep running in the background.<br>
    **-p 5000:5000**: Maps port 5000 of the host to port 5000 on the container. <br>
    **-v $(pwd)/uploads:/uploads**: Mounts the uploads directory from your current working directory to /uploads in the container


5. Access your application <br>
The application should now be accessible at `http://localhost:5000`
<hr>

### API Endpoints
#### Authentication
- **POST** /signup: Sign up a new user
- **GET** /verify-email/<token>: Verify user's email
- **POST** /login: Log in a user

#### File Operations
- **POST** /upload: Upload a file (Operation Users only)
- **GET** /files: List all uploaded files
- **GET** /download/<file_id>: Generate a download link for a file
- **GET** /secure-download/<token>: Download a file using a secure token
<hr>

### Testing
To run the test suite:
```shell
pytest -v tests/
```
You can check out a previous pytest log at [tests/test_results.log](tests/test_results.log) <br>
View the postman tests run summary at [assets/Secure File Sharing System.postman_test_run.json](assets/Secure File Sharing System.postman_test_run.json) <br>
[![Tests Summary](assets/Postman Test Summary.png)](assets/Postman Test Summary.png) <br>

You can also import the Postman collection at [assets/Secure File Sharing System.postman_collection.json](assets/Secure File Sharing System.postman_collection.json)
<hr>

### Security Considerations
- File types are verified by content, not just extension
- Download URLs are encrypted and have a short expiration time
- User passwords are hashed before storage
<hr>

### Future Improvements
- Implement rate limiting
- Add file encryption at rest
- Implement more granular user permissions
- Add logging and monitoring
<hr>

### Contributing
This project was created as part of an assessment. However, if you have suggestions or improvements, please feel free to open an issue or submit a pull request.
<hr>

### License
MIT License
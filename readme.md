To run these scripts, you will need to have both PostgreSQL and MongoDB installed on your system. You can then run the following command to start the FastAPI server:

uvicorn app:app --host 0.0.0.0 --port 8000
Once the server is started, you can then access the API at http://localhost:8000/register and http://localhost:8000/users/{user_id}.
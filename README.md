# Co-Pilot Experience for Prior Authorization

This project implements a co-pilot experience for Prior Authorization.

View instructions for completing this take-home assignment [here](https://co-helm.notion.site/Senior-Product-Engineer-Take-Home-6e82ec45cc2a46b59a0d9ee3aeb9449c).

## Tech Stack

Frontend: SvelteKit
Backend: Python (FastAPI/Django). Please start the backend first.
Database: In memory dictionary

This repo contains the code for the take home assignment

- frontend
- backend

### Requirements

Node.js 18 and above
Python environment 3.9 and above with FastAPI/
Docker

To run the backend run the following in this directory:

```bash
docker build -t my-fastapi-app .
docker run -d -p 8000:80 my-fastapi-app
```

After the backend starts navigate to frontend/ directory and run the following:

```bash
npm install
npm run dev
```

Ensure that you have node.js or above.

The project should be up and running at http://localhost:5173/

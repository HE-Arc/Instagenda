<p align="center"><a href="https://instagenda.k8s.ing.he-arc.ch//" target="_blank"><img src="https://github.com/HE-Arc/Instagenda/blob/dev/frontend/public/assets/images/logo_slogan.png?raw=true" width="400" alt="Laravel Logo"></a></p>

## About INSTAGENDA

Instagenda is a project developed by students from HE-Arc engineering school in Switzerland. The goal of this project is to create a web application that allows users to schedule Instagram posts, including media and text. The posts are automatically published when the scheduled time is reached, with team management via the Meta Graph API.

## Launch the project locally

### Prerequisites

- Python 3.13.1 or higher
    - https://www.python.org/doc/
- Node.js 18.0 or higher
    - https://nodejs.org/fr
- Tested with postgresql 17.4 or higher
    - https://www.postgresql.org/
- Docker 4.22.0 or higher
    - https://www.docker.com/get-started/

### How to start

1. **Clone the Repository**
    ```bash
   git clone git@github.com:HE-Arc/Instagenda.git
    ```
2. **Set Up Environment Variables**  
   Copy `.env.exemple` to `.env` and update the configuration as needed.  
   ```bash
   cd ./api/instagenda
   cp .env.exemple .env

   cd ../../frontend
   cp .env.exemple .env
    ```
3. **Start Backend Services**  
   ```bash
   cd ./api
   docker compose up -d
    ```
4. **Install Python Dependencies**  
   ```bash
   pip install pipenv
   pipenv install
    ```
5. **Activate the Virtual Environment**
   ```bash
   pipenv shell
    ```
6. **Run migrations and run the Backend Server**  
   ```bash
   cd ./api
   python manage.py migrate
   python manage.py runserver
    ```
7. **Set Up and Start the Frontend**  
   ```bash
    cd ./frontend
    npm i
    npm run dev
    ```

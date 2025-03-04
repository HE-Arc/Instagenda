<p align="center"><a href="https://instagenda.k8s.ing.he-arc.ch//" target="_blank"><img src="https://github.com/HE-Arc/Instagenda/blob/dev/frontend/public/assets/images/logo_slogan.png?raw=true" width="400" alt="Laravel Logo"></a></p>

## About INSTAGENDA

Instagenda is a project developed by students from HE-Arc engineering school in Switzerland. The goal of this project is to create a web application that allows users to schedule Instagram posts, including media and text. The posts are automatically published when the scheduled time is reached, with team management via the Meta Graph API.

## Launch the project locally

### Prerequisites

- Phyton 3.13.1 or higher
- Node.js 18.0 or higher
- Tested with postgresql 17.4 or higher
- Docker 4.22.0 or higher

### How to start

### How to Start

1. **Clone the Repository**
    ```bash
   git clone git@github.com:HE-Arc/Instagenda.git
    ```
2. **Set Up Environment Variables**  
   Copy `.env.example` to `.env` and update the configuration as needed.  
   ```bash
   cp .env.example .env
    ```
3. **Start Backend Services (Run in /api)**  
   ```bash
   Start Backend Services (Run in /api)
    ```
4. **Install Python Dependencies**  
   ```bash
   pipenv install
    ```
5. **Run migrations and run the Backend Server (Run in /api)**  
   ```bash
   python manage.py migrate
   python manage.py runserver
    ```
6. **Set Up and Start the Frontend (Run in /frontend)**  
   ```bash
    npm i
    npm run dev
    ```
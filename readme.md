# Ollama API Gateway with FastAPI and Nginx

This project provides a secure and efficient API gateway for the [Ollama](https://ollama.ai/) service using **Docker Compose**. This API gateway includes the following components:

* **Ollama:** Runs the large language model (LLM) service.
* **FastAPI API Gateway:** A Python application that authenticates API keys and forwards requests to Ollama.
* **Nginx Reverse Proxy:** Handles all incoming external traffic, manages timeouts, and redirects requests to the API Gateway.

This architecture helps to secure your Ollama service by not exposing it directly to the internet, while also adding a layer of control and security.

---

### Requirements

To run this project, you need to have **Docker** and **Docker Compose** installed on your computer.

---

### Setup and Configuration

#### 1. Create the .env file

This project uses a `.env` file to manage environment variables. This is a best practice for keeping secrets (like API keys) out of your code.

Create a file named `.env` in the root of your project and add the following content:

```ini
API_SECRET_KEY=your_secure_random_key_here
OLLAMA_URL=http://ollama:11434
```

**Note:** Remember to replace `your_secure_random_key_here` with a strong, random secret key.

#### 2. Update docker-compose.yml

Modify the `api-gateway` service in your `docker-compose.yml` file to use the `.env` file. Replace the `environment` section with `env_file: .env`.

```yaml
# ... (other services)
  api-gateway:
    build: ./api-gateway
    container_name: api-gateway
    depends_on:
      - ollama
    # This service will listen on the internal Docker network.
    # Nginx will forward external requests to it.
    env_file: .env
    restart: unless-stopped
# ... (other services)
```

---

### Installation and Execution

Follow these steps to start the entire system:

1.  **Clone the source code:**
    ```sh
    git clone <URL_OF_THE_SOURCE_CODE>
    cd <PROJECT_DIRECTORY_NAME>
    ```

2.  **Start the services:**
    From the project's root directory, run the following command. This will automatically download necessary images and start all services.
    ```sh
    docker-compose up -d
    ```

3.  **Pull an Ollama model:**
    The API gateway will return an error if Ollama doesn't have a model loaded. After the containers are running, execute the following command to download the `llama2` model.

    ```sh
    docker exec -it ollama-server ollama pull llama2
    ```
    This may take some time depending on your network speed.

---

### API Usage

After the containers are running and the model has been pulled, your API gateway will be available on port `8000`.

* **Endpoint:** `POST http://localhost:8000/api/generate`
* **Authentication:** You must provide an `X-API-Key` header with the secret key you defined in your `.env` file.

You can use the following `curl` command to test the API. Remember to replace `your_secret_key_here` with the value from your `.env` file.

```sh
curl http://localhost:8000/api/generate \
-H "X-API-Key: your_secret_key_here" \
-d '{
    "model": "llama2",
    "prompt": "Why is the sky blue?",
    "stream": true
}'
```

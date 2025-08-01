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

### Installation and Execution

Follow these steps to start the entire system:

1.  **Clone the source code:**
    ```sh
    git clone <URL_OF_THE_SOURCE_CODE>
    cd <PROJECT_DIRECTORY_NAME>
    ```

2.  **Start the services:**
    From the project's root directory, run the following command. This command will automatically download the necessary images, build the `api-gateway`, and start all the services.
    ```sh
    docker-compose up -d
    ```

---

### API Usage

After the containers are running, your API gateway will be available on port `8000`.

* **Endpoint:** `POST http://localhost:8000/api/generate`
* **Authentication:** You must provide an `X-API-Key` header with the value `your_secret_key_here` (or the value you changed in the `docker-compose.yml` file).

You can use the following `curl` command to test the API. Remember to replace `your_secret_key_here` and `llama2` with the appropriate values.

```sh
curl http://localhost:8000/api/generate \
-H "X-API-Key: your_secret_key_here" \
-d '{
    "model": "llama2",
    "prompt": "Why is the sky blue?",
    "stream": true
}'
```

## Whats happening?

### The Model

The model I am using is currently GPT-2. Which is initially loaded from huggingface, and optimized using huggingface's optimum package. Under the hood it uses onnx and onnx runtime. The model head we use is the GPT2LMHeadModel from the transformers library which allows us to generate a set of tokens given some initial prompt.

The model is loaded into memory before celery or fast api apps are initialized.

### Celery and FastAPI

We use celery along with rabbitmq and redis for task management. The fastAPI app route (Broker) will start a text generation task given some prompt and other arguments. A task with this info is then pushed into the rabbitmq message queue (Broker), where an available celery worker (Consumer) will use the GPT2 model loaded in memory to generate tokens given the task's data. The task results will then be stored in redis (Backend) where another fastAPI route can fetch the results using a given task id. The celery workers run concurrently allowing us to efficiently execute model inferences.

### Docker

Here we have a Dockerfile that will run all pip installs and copy the current working dir. Its final step is to execute the shell file called start_app.sh which is in charge of starting the celery server (including loading the GPT2 model in the onnx runtime) and fastAPI app.

There also exists a docker-compose.yml which will build a local rabbitmq image and an image for the current project. It is okay if rabbitmq loads after the project has loaded, as celery will send constant requests to rabbitmq for a short duration before timing out. If rabbitmq loads before timing out then all is well. Additionally the project will have to load the model into memory which will take much longer than initializing rabbitmq.

Before running the project locally ensure that you have docker and docker-compose installed.

To run the project locally execute the command:
docker-compose up -d --build

# Capstone project for "Deploy" module of HardML course

Aim of the project is to design and develop a recommendation system.
The system should find similar questions from "Quora Question Pairs" dataset.
Also the system should implement a mechanism for its seamless updating.

### Main components
The developed system consists on several main parts:

- **API Gateway** is entry point of the solution that routes user's queries and manages services communication;
- **Embedding serving** calculates universal sentence embedding of incoming sentences;
- **Cluster nodes** keep pre-calculates index of questions' embeddings and return several most similar questions for each query.
Each cluster node is described by centroid of embeddings' cluster.
- **Simple Storage Service (S3)** keeps data for API Gateway and cluster node services.



---------------
Tg @x00dr
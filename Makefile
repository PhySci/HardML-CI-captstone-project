build_base:
	docker build --tag qa:base --file ${PWD}/docker/base.Dockerfile ${PWD}/docker

build_all: build_base
	docker build --tag emb_serving:0.1 ${PWD}/src/emb_serving
	docker build --tag cluster_node:0.1 ${PWD}/src/cluster_node
	docker build --tag api-gateway:0.1 ${PWD}/src/api-gateway

run:
	docker stack deploy --compose-file compose1.yml qa

update:
	docker stack deploy --compose-file compose2.yml qa
	sleep 60 && \
    docker service update --publish-rm 9910:8000 qa_api_gateway_dg1 && \
    docker service update --publish-add 9910:8000 qa_api_gateway_dg2 && \
    sleep 60
	docker service rm qa_cluster1_dg1
	docker service rm qa_cluster2_dg1
	docker service rm qa_cluster3_dg1
	docker service rm qa_cluster4_dg1


stop:
	docker stack rm qa



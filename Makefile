IMAGE = localhost:32000/hwp
build:
	docker build -t $(IMAGE):${VERSION} .

push: build
	docker push $(IMAGE):${VERSION}

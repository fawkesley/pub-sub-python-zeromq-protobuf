.PHONY: all
all: zpubsub/pb/price_update_pb2.py

.PHONY: clean
clean:
	rm -f zpubsub/pb/price_update_pb2.py

zpubsub/pb/price_update_pb2.py: zpubsub/pb/price_update.proto
	protoc -I=zpubsub --python_out=zpubsub zpubsub/pb/price_update.proto

.PHONY: run_publisher
run_publisher:
	python -m zpubsub.publisher.publisher

.PHONY: run_subscriber
run_subscriber:
	python -m zpubsub.subscriber.subscriber

.PHONY: all
all: zpubsub/pb/price_update_pb2.py

.PHONY: clean
clean:
	rm -f zpubsub/pb/price_update_pb2.py

zpubsub/pb/price_update_pb2.py: zpubsub/pb/price_update.proto
	protoc -I=zpubsub --python_out=zpubsub zpubsub/pb/price_update.proto

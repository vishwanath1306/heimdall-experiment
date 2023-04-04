
CC = gcc
CFLAGS = -I/usr/local/include
LIBS = -L/usr/local/lib -ltracer -lprotobuf-c
PROTO_FILES = tracepoint.pb-c.c tracepoint.pb-c.h

proto: 
	protoc --c_out=. tracepoint.proto

clean: 
	rm *.o

tracepoint: 
	gcc hindsight_example.c $(PROTO_FILES) $(LIBS) -o hs_e.o
CC = gcc
CFLAGS = -Wall -Wextra -g -c -o
LFLAG = -L ./lib/
IFLAG = -I ./include/

## Directorios ##
SRC = ./src
SRCL = ./srclib
INC = ./include
BIN = ./bin
OBJ = ./obj
LIB = ./lib


# 	$^ Equivale a todas las dependencias de la regla, con un espacio entre ellas.
# 	$< Nombre de la primera dependencia de la regla.
# 	$@ Nombre del fichero destino de la regla.
# 	(Para enlazar bibliotecas, estas se ponen a la derecha del todo)

.PHONY: all librerias directorios clean rm_dir

all: directorios librerias $(OBJ)/peticiones_http.o $(OBJ)/socket.o $(OBJ)/servidor.o $(BIN)/servidor 

librerias: $(OBJ)/picohttpparser.o $(LIB)/libpicohttpparser.a
directorios: 
	mkdir -p $(OBJ)/
	mkdir -p $(LIB)/
	mkdir -p $(BIN)/

## Ejecutables ## 
$(BIN)/servidor: $(OBJ)/servidor.o $(OBJ)/socket.o $(OBJ)/peticiones_http.o
	$(CC) -o $@ $^ -pthread -lpicohttpparser $(LFLAG)

## Objetos ##
$(OBJ)/socket.o: $(SRC)/socket.c $(INC)/socket.h 
	$(CC) $(CFLAGS) $@ $< $(IFLAG)

$(OBJ)/servidor.o: $(SRC)/servidor.c $(INC)/include_general.h
	$(CC) $(CFLAGS) $@ $< $(IFLAG)

$(OBJ)/picohttpparser.o: $(SRCL)/picohttpparser.c $(INC)/picohttpparser.h
	$(CC) $(CFLAGS) $@ $< $(IFLAG)

$(OBJ)/peticiones_http.o: $(SRC)/peticiones_http.c $(INC)/peticiones_http.h 
	$(CC) $(CFLAGS) $@ $< $(IFLAG)


## Librerias ##
$(LIB)/libpicohttpparser.a: $(OBJ)/picohttpparser.o
	ar -crs $@ $<

clean:
	rm -f $(OBJ)/*.o $(BIN)/* $(LIB)/* 

rm_dir: 
	rm -rf $(OBJ) $(LIB) $(BIN)

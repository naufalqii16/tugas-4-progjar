import socket
import json
import base64
import logging
import os

server_address = ('0.0.0.0', 6666)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received = ""  # empty string
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {str(e)}")
        return False

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        return True
    else:
        print("Gagal")
        return False

def remote_upload(path=""):
    try:
        with open(path, 'rb') as f:
            file_contents = f.read()
            encoded_contents = base64.b64encode(file_contents).decode()
        name = os.path.basename(path)
        command_str = f"UPLOAD {encoded_contents} {name}"
        hasil = send_command(command_str)
        if hasil.get('status') == 'OK':
            print(hasil)
            return True
        else:
            print(hasil)
            return False
    except Exception as e:
        logging.warning(f"error during file upload: {str(e)}")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print("File berhasil dihapus")
        return True
    else:
        print(hasil)
        return False

if __name__ == '__main__':
    server_address = ('localhost', 6666)
    while True:
        command = input("Enter command: ")
        if command.startswith("LIST"):
            remote_list()
        elif command.startswith("GET"):
            filename = command.split(" ")[1]
            remote_get(filename)
        elif command.startswith("UPLOAD"):
            path = command.split(" ")[1]
            remote_upload(path)
        elif command.startswith("DELETE"):
            filename = command.split(" ")[1]
            remote_delete(filename)
        else:
            print("Invalid command")

from reedsolo import RSCodec, ReedSolomonError

rsc = RSCodec(204)

def Encoder(data0):
    length = len(data0)
    last_length = length % 51
    chunks = round(length / 51)+1
    data = data0 + ("0"*(102-last_length)).encode('utf-8')
    dataArray = []
    for i in range(chunks):
        dataArray.append(bytes(rsc.encode(data[i*51 : (i+1)*51])))
    if chunks == 0:
        dataArray.append(bytes(rsc.encode(data)))
    with open("log.txt" , "w") as file:
        file.write(str(length))
    return dataArray

def interleaver(dataArray):
    storage_data = []
    for i in range(255):
        storage_data.append(bytes(bytearray(dataArray[x][i] for x in range(len(dataArray)))))
    return storage_data

def save_files(storage_data):
    for i in range(255):
        with open(f"encoded_data{i}", "wb") as file:
            file.write(storage_data[i])

def load_files():
    storage_data = []
    for i in range(255):
        with open(f"encoded_data{i}", "rb") as file:
            storage_data.append(file.read())
    return storage_data

def deinterleaver(storage_data):
    chunks = len(storage_data[0])
    dataArray = []
    for i in range(chunks):
        dataArray.append(bytes(bytearray(storage_data[x][i] for x in range(255))))
    return dataArray

def Decoder(dataArray):
    with open("log.txt" , "r") as file:
        length = int(file.read())
    chunks = round(length / 51)+1
    if chunks == 0:
        return bytes(rsc.decode(dataArray[0])[0])[:length]
    for i in range(chunks):
        if i == 0:
            globals()[f"data{i}"] = bytes(rsc.decode(dataArray[i])[0])
        else:
            globals()[f"data{i}"] = globals()[f"data{i-1}"] + bytes(rsc.decode(dataArray[i])[0])
    globals()[f"data{i}"] = globals()[f"data{i}"][:length]
    return globals()[f"data{i}"]


if __name__ == "__main__":
    #Encoder side
    with open(f"x.py", 'rb') as file:
        Raw_data = file.read()
    dataArray= Encoder(Raw_data)
    storage_data = interleaver(dataArray)
    save_files(storage_data)

    #Decoder side
    storage_data = load_files()
    dataArray = deinterleaver(storage_data)
    data = Decoder(dataArray)
    with open(f"y.py", 'wb') as file:
        file.write(data)

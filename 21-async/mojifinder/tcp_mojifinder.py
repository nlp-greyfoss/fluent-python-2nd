import asyncio
import functools
import sys
from asyncio.trsock import TransportSocket
from typing import cast
from charindex import InvertedIndex, format_results


CRLF = b'\r\n'
PROMPT = b'?> '

async def finder(index: InvertedIndex,  # 
                reader: asyncio.StreamReader,
                writer: asyncio.StreamWriter) -> None:
    client = writer.get_extra_info('peername') # 
    while True:
        writer.write(PROMPT) # 不能用await
        await writer.drain() # 必须用await
        data = await reader.readline() # readline是一个返回bytes的协程方法
        if not data:
            break
        try:
            query = data.decode().strip()
        except UnicodeDecodeError: # 当用户按下Ctrl-C或客户端发送控制字节
            query = '\x00'
        print(f' From {client}: {query!r}') # 打印
        if query:
            if ord(query[:1]) < 32: # 如果控制或空字符被收到
                break

            results = await search(query, index, writer)  # 进行真正的搜索
            print(f' To {client}: {results} results.')

    writer.close() # 关闭StreamWriter
    await writer.wait_closed() # 等待StreamWriter关闭
    print(f'Close {client}.') # 


async def supervisor(index: InvertedIndex, host: str, port: int) -> None:
    server = await asyncio.start_server( # 快速构建一个asyncio.Server(TCP socket服务器)
        functools.partial(finder, index), # start_server的一个参数是client_connected_callback，用partialWiefinder绑定参数index
        host, port) # start_server的第二个参数和第三个参数是host和port
    
    socket_list = cast(tuple[TransportSocket, ...], server.sockets) 
    addr = socket_list[0].getsockname()
    print(f'Serving on {addr}. Hit CTRL-C to stop.')  
    await server.serve_forever() # 让supervisor在此处阻塞运行


async def search(query: str, index: InvertedIndex, writer: asyncio.StreamWriter) -> int: # 因为StreamWriter是异步的，所以该函数也必须是async的
    chars = index.search(query) 
    lines = (line.encode() + CRLF for line in format_results(chars)) 

    writer.writelines(lines) # 写多行，该方法不是协程
    await writer.drain() # 但drain方法是协程
    status_line = f'{"─" * 66} {len(chars)} found' 
    writer.write(status_line.encode() + CRLF)
    await writer.drain()
    return len(chars)

def main(host: str = "127.0.0.1", port_arg: str = "2323"):
    port = int(port_arg)
    print("Building index.")
    index = InvertedIndex()
    try:
        asyncio.run(supervisor(index, host, port))  # 开启event loop ，运行supervisor
    except KeyboardInterrupt: 
        print('\nBye.')
    
if __name__ == '__main__':
    main(*sys.argv[1:])
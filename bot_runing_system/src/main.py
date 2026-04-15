import glob
import sys
sys.path.insert(0, glob.glob('../../')[0])

from bot_run_server.bot_run_service import BotRun

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class CalculatorHandler:
    print("bot_runing_server")
    def add_bot(self,id,botId,bot_code,input,channel_name):
        print(id,botId,bot_code,input,channel_name)
        return 0


if __name__ == '__main__':
    handler = CalculatorHandler()
    processor = BotRun.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9091)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    # server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    server = TServer.TThreadedServer(
        processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Starting the server...')
    server.serve()
    print('done.')
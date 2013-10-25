'''Created by Dmytro Konobrytskyi, 2012(C)'''
from RCP2Router.Router import Router
from RCP2Console.Console import Console

import thread
from RCP2Router.StreamsCollector import StreamsCollector
 
def RouterThreadFunc():
    router = Router("tcp://127.0.0.1:55557", "tcp://127.0.0.1:55559")
    router.Run();
    
def StreamsCollectorThreadFunc():
    streamsCollector = StreamsCollector("tcp://127.0.0.1:55559")
    streamsCollector.Run();
    
if __name__ == '__main__':
    thread.start_new_thread(RouterThreadFunc, ())
    thread.start_new_thread(StreamsCollectorThreadFunc, ())
    console = Console("tcp://127.0.0.1:55559")

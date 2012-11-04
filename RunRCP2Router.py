'''Created by Dmytro Konobrytskyi, 2012(C)'''
from RCP2Router.Router import Router

if __name__ == '__main__':
    router = Router("tcp://127.0.0.1:55557", "tcp://127.0.0.1:55559")
    router.Run();
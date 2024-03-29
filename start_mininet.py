from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

NET = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
# configuracao da nat

def init_clients():
        
        cliente01 = NET.addHost( 'cliente01', ip="10.0.1.2/24", mac="00:00:00:00:00:01" )   #host cliente chatBot
        cliente02 = NET.addHost( 'cliente02', ip="10.0.2.2/24", mac="00:00:00:00:00:02" )   #host servidor chatBot
        cliente03 = NET.addHost( 'cliente03', ip="10.0.3.2/24", mac="00:00:00:00:00:03" )   #host link externo
        
        return cliente01, cliente02, cliente03
        
def init_routers():
        roteador1 = NET.addHost( 'roteador1')
        roteador2 = NET.addHost( 'roteador2')
        roteador3 = NET.addHost( 'roteador3')
        
        return roteador1, roteador2, roteador3
        
def add_routes_client1(cliente01):
        cliente01.cmd("route add -host 10.0.2.2 gw 10.0.1.1 dev cliente01-eth0")    # rota para cliente02 
        cliente01.cmd("route add -host 10.0.3.2 gw 10.0.1.1 dev cliente01-eth0")    # rota para cliente03  
        cliente01.cmd("route add -host 10.0.10.1 gw 10.0.1.1 dev cliente01-eth0")   # rota para roteador1-eth0 
        cliente01.cmd("route add -host 10.0.10.2 gw 10.0.1.1 dev cliente01-eth0")   # rota para roteador2-eth0 
        cliente01.cmd("route add -host 10.0.20.1 gw 10.0.1.1 dev cliente01-eth0")   # rota para roteador2-eth1
        cliente01.cmd("route add -host 10.0.2.1 gw 10.0.1.1 dev cliente01-eth0")    # rota para roteador2-eth2 
        cliente01.cmd("route add -host 10.0.20.2 gw 10.0.1.1 dev cliente01-eth0")   # rota para roteador3-eth0
        cliente01.cmd("route add -host 10.0.3.1 gw 10.0.1.1 dev cliente01-eth0")    # rota para roteador3-eth1
        
        return cliente01

def add_routes_client2(cliente02):
        cliente02.cmd("route add -host 10.0.1.2 gw 10.0.2.1 dev cliente02-eth0")    # rota para cliente01 
        cliente02.cmd("route add -host 10.0.3.2 gw 10.0.2.1 dev cliente02-eth0")    # rota para cliente03
        cliente02.cmd("route add -host 10.0.10.1 gw 10.0.2.1 dev cliente02-eth0")   # rota para roteador1-eth0
        cliente02.cmd("route add -host 10.0.1.1 gw 10.0.2.1 dev cliente02-eth0")    # rota para roteador1-eth1
        cliente02.cmd("route add -host 10.0.10.2 gw 10.0.2.1 dev cliente02-eth0")   # rota para roteador2-eth0
        cliente02.cmd("route add -host 10.0.20.1 gw 10.0.2.1 dev cliente02-eth0")   # rota para roteador2-eth1
        cliente02.cmd("route add -host 10.0.20.2 gw 10.0.2.1 dev cliente02-eth0")   # rota para roteador3-eth0
        cliente02.cmd("route add -host 10.0.3.1 gw 10.0.2.1 dev cliente02-eth0")    # rota para roteador3-eth1
        
        return cliente02

def add_routes_client3(cliente03):
        cliente03.cmd("route add -host 10.0.1.2 gw 10.0.3.1 dev cliente03-eth0")    # rota para cliente01
        cliente03.cmd("route add -host 10.0.2.2 gw 10.0.3.1 dev cliente03-eth0")    # rota para cliente02
        cliente03.cmd("route add -host 10.0.10.1 gw 10.0.3.1 dev cliente03-eth0")   # rota para roteador1-eth0
        cliente03.cmd("route add -host 10.0.1.1 gw 10.0.3.1 dev cliente03-eth0")    # rota para roteador1-eth1
        cliente03.cmd("route add -host 10.0.10.2 gw 10.0.3.1 dev cliente03-eth0")   # rota para roteador2-eth0
        cliente03.cmd("route add -host 10.0.20.1 gw 10.0.3.1 dev cliente03-eth0")   # rota para roteador2-eth1
        cliente03.cmd("route add -host 10.0.2.1 gw 10.0.3.1 dev cliente03-eth0")    # rota para roteador2-eth2
        cliente03.cmd("route add -host 10.0.20.2 gw 10.0.3.1 dev cliente03-eth0")   # rota para roteador3-eth0
        
        return cliente03

def config_router1(roteador1):
        roteador1.cmd("ifconfig roteador1-eth0 0")
        roteador1.cmd("ifconfig roteador1-eth1 0")
        roteador1.cmd("ifconfig roteador1-eth0 hw ether 00:00:00:00:01:12")     # adiciona end. MAC para interface eht0
        roteador1.cmd("ifconfig roteador1-eth1 hw ether 00:00:00:00:01:01")     # adiciona end. MAC para interface eht1
        roteador1.cmd("ip addr add 10.0.10.1/24 brd + dev roteador1-eth0")  # seta IP e broadcast na interface eth0
        roteador1.cmd("ip addr add 10.0.1.1/24 brd + dev roteador1-eth1")   # seta IP e broadcast na interface eth1
        
        return roteador1

def config_router2(roteador2):
        roteador2.cmd("ifconfig roteador2-eth0 0")
        roteador2.cmd("ifconfig roteador2-eth1 0")
        roteador2.cmd("ifconfig roteador2-eth2 0")
        roteador2.cmd("ifconfig roteador2-eth0 hw ether 00:00:00:00:02:12")     # adiciona end. MAC para interface eht0
        roteador2.cmd("ifconfig roteador2-eth1 hw ether 00:00:00:00:02:23")     # adiciona end. MAC para interface eht1
        roteador2.cmd("ifconfig roteador2-eth2 hw ether 00:00:00:00:02:01")     # adiciona end. MAC para interface eht2
        roteador2.cmd("ip addr add 10.0.10.2/24 brd + dev roteador2-eth0")  # seta IP e broadcast na interface eth0
        roteador2.cmd("ip addr add 10.0.20.1/24 brd + dev roteador2-eth1")  # seta IP e broadcast na interface eth1
        roteador2.cmd("ip addr add 10.0.2.1/24 brd + dev roteador2-eth2")   # seta IP e broadcast na interface eth2
        
        return roteador2
    
def config_router3(roteador3):
        roteador3.cmd("ifconfig roteador3-eth0 0")
        roteador3.cmd("ifconfig roteador3-eth1 0")
        roteador3.cmd("ifconfig roteador3-eth0 hw ether 00:00:00:00:03:23")     # adiciona end. MAC para interface eht0
        roteador3.cmd("ifconfig roteador3-eth1 hw ether 00:00:00:00:03:01")     # adiciona end. MAC para interface eht1
        roteador3.cmd("ip addr add 10.0.20.2/24 brd + dev roteador3-eth0")  # seta IP e broadcast na interface eth0
        roteador3.cmd("ip addr add 10.0.3.1/24 brd + dev roteador3-eth1")   # seta IP e broadcast na interface eth1
        
        return roteador3

def add_routes_router1(roteador1):
        roteador1.cmd("route add -host 10.0.2.2 gw 10.0.10.2 dev roteador1-eth0")   # rota para cliente02
        roteador1.cmd("route add -host 10.0.3.2 gw 10.0.10.2 dev roteador1-eth0")   # rota para cliente03
        roteador1.cmd("route add -host 10.0.20.1 gw 10.0.10.2 dev roteador1-eth0")  # rota para roteador2-eth1
        roteador1.cmd("route add -host 10.0.2.1 gw 10.0.10.2 dev roteador1-eth0")   # rota para roteador2-eth2
        roteador1.cmd("route add -host 10.0.20.2 gw 10.0.10.2 dev roteador1-eth0")  # rota para roteador3-eth0
        roteador1.cmd("route add -host 10.0.3.1 gw 10.0.10.2 dev roteador1-eth0")   # rota para roteador3-eth1
        roteador1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
        
        return roteador1

def add_routes_router2(roteador2):
        roteador2.cmd("route add -host 10.0.1.2 gw 10.0.10.1 dev roteador2-eth0")   #rota para cliente01
        roteador2.cmd("route add -host 10.0.3.2 gw 10.0.20.2 dev roteador2-eth1")   #rota para cliente03
        roteador2.cmd("route add -host 10.0.1.1 gw 10.0.10.1 dev roteador2-eth0")   #rota para roteador1-eth1
        roteador2.cmd("route add -host 10.0.3.1 gw 10.0.20.2 dev roteador2-eth1")   #rota para roteador3-eth1
        roteador2.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
        
        return roteador2

def add_routes_router3(roteador3):
        roteador3.cmd("route add -host 10.0.1.2 gw 10.0.20.1 dev roteador3-eth0")   # rota para cliente01
        roteador3.cmd("route add -host 10.0.2.2 gw 10.0.20.1 dev roteador3-eth0")   # rota para cliente02
        roteador3.cmd("route add -host 10.0.10.1 gw 10.0.20.1 dev roteador3-eth0")  # rota para roteador1-eth0
        roteador3.cmd("route add -host 10.0.1.1 gw 10.0.20.1 dev roteador3-eth0")   # rota para roteador1-eth1
        roteador3.cmd("route add -host 10.0.10.2 gw 10.0.20.1 dev roteador3-eth0")  # rota para roteador2-eth0
        roteador3.cmd("route add -host 10.0.2.1 gw 10.0.20.1 dev roteador3-eth0")   # rota para roteador2-eth2
        roteador3.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
        
        return roteador3
        
def start_topology():
        # Adiciona hosts-ok
        client1, client2, client3 = init_clients()

        # Adiciona roteadores
        router1, router2, router3 = init_routers()

        # Adiciona enlaces entre os roteadores
        NET.addLink( router1, router2 )
        NET.addLink( router2, router3 )

        #Adiciona enlaces entre hosts e roteadores
        NET.addLink( client1, router1 )
        NET.addLink( client2, router2 )
        NET.addLink( client3, router3 )

        NET.build()

        ################# SUBREDE 01 ################
        # rotas do cliente01 para chegar nos destinos: 
        client1 = add_routes_client1(client1)

        # configuracoes roteador1-
        router1 = config_router1(router1)
    
        # rotas do roteador1 para chegar nos destinos:
        router1 = add_routes_router1(router1)
        
        
        ################# SUBREDE 02 ################
        # rotas do cliente02 para chegar nos destinos:
        client2 = add_routes_client2(client2)
        

        # configuracoes roteador2-
        router2 = config_router2(router2)

        # rotas do roteador2 para chegar nos destinos:
        router2 = add_routes_router2(router2)
        

        ################# SUBREDE 03 ################
        # rotas do cliente03 para chegar nos destinos:
        client3 = add_routes_client3(client3)

        # configuracoes roteador3-
        router3 = config_router3(router3)

        # rotas do roteador3 para chegar nos destinos:
        router3 = add_routes_router3(router3)

        
        
        print "*** Rede Iniciada ***"
        CLI( NET )      # inicia rede com todas as configuracoes setadas

        print "*** Rede finalizada ***"
        NET.stop()      # finaliza rede

if __name__ == '__main__':
    setLogLevel( 'info' )
    start_topology() 

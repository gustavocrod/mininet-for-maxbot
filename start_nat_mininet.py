from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.nodelib import NAT
from mininet.topo import Topo

NAT_IP = '10.0.3.2'
            
class MiniTopo():
      def build(self):  

        ##### inicializacao dos hots #####
        
        client1 = self.addHost( 'cliente01', ip='10.0.1.2', defaultRoute='via ' + NAT_IP )   #host cliente chatBot
        client2 = self.addHost( 'cliente02', ip='10.0.2.2', defaultRoute='via ' + NAT_IP )   #host servidor chatBot
        client3 = self.addNode( 'cliente03', cls=NAT, ip=NAT_IP, inNamespace=False ) # configuracao da nat
        ##### Configracao dos switchs (roteadores) #####
        router1 = self.addSwitch( 'roteador1' )
        router2 = self.addSwitch( 'roteador2' )
        router3 = self.addSwitch( 'roteador3' )

        # Adiciona enlaces entre os roteadores
        self.addLink( router1, router2 )
        self.addLink( router2, router3 )

        #Adiciona enlaces entre hosts e roteadores
        self.addLink( client1, router1 )
        self.addLink( client2, router2 )
        self.addLink( client3, router3 )

        
def start_topology():
        topo = MiniTopo()
        net = Mininet(topo=topo)
        
        net.start()

        print "*** Rede Iniciada ***"
        CLI( NET )      # inicia rede com todas as configuracoes setadas

        print "*** Rede finalizada ***"
        net.stop()      # finaliza rede

if __name__ == '__main__':
    setLogLevel( 'info' )
    start_topology() 

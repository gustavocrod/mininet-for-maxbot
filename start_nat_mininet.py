from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.nodelib import NAT
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
            
class MiniTopo(Topo):
      def build(self, NAT_IP='10.0.0.5'):  

        ##### inicializacao dos hots #####
        
        client1 = self.addHost( 'cliente1', ip='10.0.0.1/24', defaultRoute='via ' + NAT_IP )   # host cliente chatBot
        client2 = self.addHost( 'cliente2', ip='10.0.0.2/24', defaultRoute='via ' + NAT_IP )   # host servidor chatBot
        client3 = self.addNode( 'cliente3', cls=NAT, ip=NAT_IP + '/24', inNamespace=False ) # configuracao da nat
 
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
        net = Mininet(topo)
        
        net.start()

        print "*** Rede Iniciada ***"
        CLI( net )      # inicia rede com todas as configuracoes setadas

        print "*** Rede finalizada ***"
        net.stop()      # finaliza rede

if __name__ == '__main__':
    setLogLevel( 'info' )
    start_topology() 

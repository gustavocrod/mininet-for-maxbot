#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.nodelib import NAT
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.util import irange

class InternetTopo(Topo):
    "1 switch connectado com n hosts."
    def build(self, n=2, **_kwargs ):
        # config do switch q conecta com o externo
        internetRouter = self.addSwitch('roteador0')
        # config do client q conecta com o externo
        internetClient = self.addHost('cliente01')
        self.addLink(internetRouter, internetClient)

        # configuracao das redes internas
        for i in irange(1, n):
            internetIface = 'nat%d-eth0' % i
            locaIface = 'nat%d-eth1' % i
            localIP = '192.168.%d.1' % i
            localSubnet = '192.168.%d.0/24' % i
            natParams = { 'ip' : '%s/24' % localIP }
            
            # adicionando NAT na topologia
            nat = self.addNode('nat%d' % i, cls=NAT, subnet=localSubnet,
                               inetIntf=internetIface, localIntf=localIface)
                               
            router = self.addSwitch('s%d' % i)
            # conecta NAT na internet e nos switches (roteadores) locais
            self.addLink(nat, internetRouter, intfName1=internetIface)
            self.addLink(nat, router, intfName1=localIface, params1=natParams)
            
            # adiciona o cliente e conecta com o roteador conectado a ele
            client = self.addHost('cliente0%d' % i,
                                ip='192.168.%d.100/24' % i,
                                defaultRoute='via %s' % localIP)
            self.addLink(client, router)

def run():
    "cria a rede e roda o CLI"
    topo = InternetTopo()
    net = Mininet(topo=topo)
    net.start()
    CLI(net)
    print "Rede iniciada"
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

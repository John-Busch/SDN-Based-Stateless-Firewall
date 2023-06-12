#!/usr/bin/python



from mininet.net import Mininet
from mininet.node import Controller, OVSSwitch, RemoteController, OVSKernelSwitch, Host
from mininet.cli import CLI
from mininet.log import setLogLevel
#Code by John Busch
def multiControllerNet():
	"Create a network from semi-scratch with multiple controllers."

	net = Mininet(topo=None, build=False, ipBase='10.0.2.0/8', autoSetMacs=True) 
	print("*** Creating controllers")
	c1 = net.addController( 'c1', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6633 )
	c2 = net.addController( 'c2', controller=RemoteController, ip='127.0.0.1', protocol='tcp', port=6655 )

	print("*** Creating switches")
	s1 = net.addSwitch( 's1', cls=OVSKernelSwitch)
	s2 = net.addSwitch( 's2', cls=OVSKernelSwitch)

	print("*** Creating hosts")
	
	h1 = net.addHost('h1', cls=Host, ip='10.0.2.10/8')
	h2 = net.addHost('h2', cls=Host, ip='10.0.2.20/8')
	h3 = net.addHost('h3', cls=Host, ip='192.168.2.30/8')
	h4 = net.addHost('h4', cls=Host, ip='192.168.2.10/8')


	print("*** Creating links")
	net.addLink(s1, h1)
	net.addLink(s1, h2)
	net.addLink(s2, h3)
	net.addLink(s2, h4)
	net.addLink(s2, h1, ip="192.168.2.10/8")

	print("*** Starting network")
	net.build()
	print("*** Starting Controllers")
	c1.start()
	c2.start()
	print("*** Starting switches")
	net.get('s1').start( [ c1 ] )
	net.get('s2').start( [ c2 ] )

	#print("*** Testing network")
	#net.pingAll()

	print("*** Running CLI")
	CLI( net )

	print("*** Stopping network")
	net.stop()

if __name__ == '__main__':
	setLogLevel( 'info' )  # for CLI output
	multiControllerNet()

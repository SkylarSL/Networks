#!/usr/bin/python

"""Topology with 10 switches and 10 hosts
"""

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.log import setLogLevel

class CSLRTopo( Topo ):

        def __init__( self ):
                "Create Topology"

                # Initialize topology
                Topo.__init__( self )

                # Add hosts
                a = self.addHost( 'alice' )
                b = self.addHost( 'bob' )
                c = self.addHost( 'carol' )
                d = self.addHost( 'david' )

                # Add switches
                s1 = self.addSwitch( 's1', listenPort=6634 )
                s2 = self.addSwitch( 's2', listenPort=6635 )
                s3 = self.addSwitch( 's3', listenPort=6636 )
                r1 = self.addSwitch( 'r1', listenPort=6637 )
                r2 = self.addSwitch( 'r2', listenPort=6638 )

                # Add links between hosts and switches
                self.addLink( a, s1 ) # alice-eth0 <-> s1-eth1
                self.addLink( b, s2 ) # bob-eth0   <-> s2-eth1
                self.addLink( c, s3 ) # carol-eth0 <-> s3-eth1
                self.addLink( d, s2 ) # david-eth0 <-> s2-eth2


                # Add links between switches, with bandwidth 100Mbps
                self.addLink( s1, r1, bw=100 ) # s1-eth2 <-> r1-eth1, Bandwidth = 100Mbps
                self.addLink( s2, r1, bw=100 ) # s2-eth3 <-> r1-eth2, Bandwidth = 100Mbps
                self.addLink( s2, r2, bw=100 ) # s2-eth4 <-> r2-eth1, Bandwidth = 100Mbps
                self.addLink( s3, r2, bw=100 ) # s3-eth2 <-> r2-eth2, Bandwidth = 100Mbps

def run():
        "Create and configure network"
        topo = CSLRTopo()
        net = Mininet( topo=topo, link=TCLink, controller=None )

        # Set interface IP and MAC addresses for hosts
        a = net.get( 'alice' )
        a.intf( 'alice-eth0' ).setIP( '10.1.1.17', 24 )
        a.intf( 'alice-eth0' ).setMAC( 'AA:AA:AA:AA:AA:AA' )

        b = net.get( 'bob' )
        b.intf( 'bob-eth0' ).setIP( '10.4.4.48', 24 )
        b.intf( 'bob-eth0' ).setMAC( 'B0:B0:B0:B0:B0:B0' )

        c = net.get( 'carol' )
        c.intf( 'carol-eth0' ).setIP( '10.6.6.69', 24 )
        c.intf( 'carol-eth0' ).setMAC( 'CC:CC:CC:CC:CC:CC' )

        d = net.get( 'david' )
        d.intf( 'david-eth0' ).setIP( '10.4.4.96', 24 )
        d.intf( 'david-eth0' ).setMAC( 'D0:D0:D0:D0:D0:D0' )

        # Set interface MAC address for switches (NOTE: IP
        # addresses are not assigned to switch interfaces)
        s1 = net.get( 's1' )
        s1.intf( 's1-eth1' ).setMAC( '0A:00:00:01:00:01' ) # Alice
        s1.intf( 's1-eth2' ).setMAC( '0A:00:00:01:00:02' ) # r1

        s2 = net.get( 's2' )
        s2.intf( 's2-eth1' ).setMAC( '0A:00:00:02:00:01' ) # Bob
        s2.intf( 's2-eth2' ).setMAC( '0A:00:00:02:00:02' ) # David
        s2.intf( 's2-eth3' ).setMAC( '0A:00:00:02:00:03' ) # r1
        s2.intf( 's2-eth4' ).setMAC( '0A:00:00:02:00:04' ) # r2

        s3 = net.get( 's3' )
        s3.intf( 's3-eth1' ).setMAC( '0A:00:00:03:00:01' ) # Carol
        s3.intf( 's3-eth2' ).setMAC( '0A:00:00:03:00:02' ) # r2

        r1 = net.get( 'r1' )
        r1.intf( 'r1-eth1' ).setMAC( '0A:00:00:04:00:01' ) # s1
        r1.intf( 'r1-eth2' ).setMAC( '0A:00:00:04:00:02' ) # s2

        r2 = net.get( 'r2' )
        r2.intf( 'r2-eth1' ).setMAC( '0A:00:00:05:00:01' ) # s2
        r2.intf( 'r2-eth2' ).setMAC( '0A:00:00:05:00:02' ) # s3

        net.start()

        # Add routing table entries for hosts (NOTE: The gateway
		# IPs 10.0.X.1 are not assigned to switch interfaces)
        a.cmd( 'route add default gw 10.1.1.14 dev alice-eth0' )
        b.cmd( 'route add default gw 10.4.4.14 dev bob-eth0' )
        c.cmd( 'route add default gw 10.6.6.46 dev carol-eth0' )
        d.cmd( 'route add default gw 10.4.4.28 dev david-eth0' )

        # Add arp cache entries for hosts
        a.cmd( 'arp -s 10.1.1.14 0A:00:00:01:00:01 -i alice-eth0' )
        b.cmd( 'arp -s 10.4.4.14 0A:00:00:02:00:01 -i bob-eth0' )
        c.cmd( 'arp -s 10.6.6.46 0A:00:00:03:00:01 -i carol-eth0' )
        d.cmd( 'arp -s 10.4.4.28 0A:00:00:02:00:02 -i david-eth0' )

        # Open Mininet Command Line Interface
        CLI(net)

        # Teardown and cleanup
        net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
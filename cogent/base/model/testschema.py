from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship, backref
import sqlalchemy.types as types
from Bitset import Bitset
import unittest
from datetime import datetime

from cogent.base.model import *

from cogent.base.model.meta import Session, Base


class TestNodeType(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        self.engine = create_engine("sqlite:///:memory:", echo=False)
        self.engine.execute("pragma foreign_keys=on")
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = Base.metadata
        self.metadata.create_all(self.engine)

        
    def test1(self):
        session = self.Session()
        b = Bitset(size=20)
        b[3] = True
        b[13] = True

        r = NodeType(time=datetime.utcnow(),
                     id=0,
                     name="base",
                     seq=1,
                     updated_seq=1,
                     period=1024*300,
                     configured=b)
        try:
            session.add(r)
            session.commit()
        except Exception,e:
            print e
            session.rollback()

        self.assertTrue( r.configured[3] and r.configured[13] )

    def test2(self):
        session = self.Session()
        b = Bitset(size=20)
        b[3] = True
        b[13] = True

        r = NodeType(time=datetime.utcnow(),
                     id=0,
                     name="base",
                     seq=1,
                     updated_seq=1,
                     period=1024*300,
                     configured=b)
        try:
            session.add(r)
            session.commit()
        except Exception,e:
            print e
            session.rollback()

        session = self.Session()
        r = session.query(NodeType).get(0)

        self.assertTrue( r.name == "base" )

            
        self.assertTrue( r.configured[3] and r.configured[13] )

    def test3(self):
        session = self.Session()
        r = session.query(NodeType).get(0)
        self.assertTrue( r is None )


class TestSchema(unittest.TestCase):
    def setUp(self):
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker

        self.engine = create_engine("mysql://james@localhost/ch_test", echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.metadata = Base.metadata
        self.metadata.drop_all(self.engine)
        self.metadata.create_all(self.engine)

    def test1(self):
        session = self.Session()

        #Add a deployment


        dep = Deployment(name="TestDep",
                         description="Does this work",
                         startDate=datetime.now()
                         , endDate=None)
        session.add(dep)
        session.commit()
        depid = dep.id

        #Add a room type

        rt = RoomType(name="Bedroom")
        session.add(rt)
        session.commit()


        #Add Deployment Meta data
        dm = DeploymentMetadata(deploymentId=depid,
                                 name="Manual Reading",
                                 description="Read something",
                                 units="kwh",
                                 value="99999")
        session.add(dm)
        session.commit()


        #Add a house
        h = House(deploymentId=1,
                  address = "1 Sampson",
                  startDate=datetime.now())

        session.add(h)
        session.commit()


        #Add house metadata

        hm = HouseMetadata(houseId=1,
                                 name="Manual Reading",
                                 description="Read something",
                                 units="kwh",
                                 value="99999")
        session.add(hm)
        session.commit()


        #Add Occupier

        occ=Occupier(houseId=1,
                     name="Mr Man",
                     contactNumber="01212342345",
                     startDate=datetime.now()
                     )

        session.add(occ)
        session.commit()

        #Add rooms
        rt_bedroom = RoomType(name="Bedroom")
        session.add(rt_bedroom)
        session.commit()
        
        r=Room(roomTypeId=rt_bedroom.id,
               name="BedroomA")
        

        session.add(r)
        session.commit()

        #Add a node
        configured = Bitset(size=14)
        configured[0] = True
        configured[2] = True
        configured[4] = True
        configured[5] = True
        configured[6] = True
        configured[13] = True
        configured1 = Bitset(size=14)
        configured1[13] = True
        session.add_all(
            [
                NodeType(time=datetime.now(),
                         id=0,
                         name="base",
                         seq=1,
                         updated_seq=0,
                         period=15*1024,
                         configured=configured),
                NodeType(time=datetime.now(),
                         id=1,
                         name="cc",
                         seq=1,
                         updated_seq=0,
                         period=15*1024,
                         configured=configured1),
                ])                    

        session.commit()

        #Add sensors

        #Add sensor types

        #Add readings

        n = Node(id=63,
                 houseId=h.id,
                 nodeTypeId=0,
                 roomId=r.id)
        session.add(n)

        st = SensorType(id=0,
                        name="Temperature",
                        code="Tmp",
                        units="deg.C")

        session.add(st)
        session.commit()

        for i in range(100):
            r = Reading(time=datetime.now(),
                        nodeId=63,
                        typeId=0,
                        value=i/1000.)
            session.add(r)
            ns = NodeState(time=datetime.now(),
                           nodeId=63,
                           parent=64,
                           localtime=( (1<<32) - 50 + i)) # test large integers
            session.add(ns)
        session.commit()

        session.close()
        session = self.Session()

        loctimes = [x[0] for x in session.query(NodeState.localtime).all()]
        print max(loctimes) - min(loctimes)
        self.assertTrue(max(loctimes) - min(loctimes) == 99) 


    #Add node history
if __name__ == "__main__":
    unittest.main()

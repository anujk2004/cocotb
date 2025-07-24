import constraint
import random
import sys
class etherconstr:
    def __init__(self):
        self.p=constraint.Problem()
        self.p.addVariable('hdrlen' ,[14,16])
        self.p.addVariable('payload' ,range(48 ,1500))
        self.p.addVariable('length' , range(64,1500))
        self.p.addVariable('type', range(0x800, 0xffff))
        self.p.addVariable('hasvlan' , [True,False])
        self.p.addConstraint(lambda len,hdr,pyld: len == hdr+pyld ,['length' ,'hdrlen' ,'payload'])
        self.p.addConstraint(lambda vlan ,hdrlen: hdrlen==16 if vlan else hdrlen == 14 ,['hasvlan','hdrlen'])
        self.p.addConstraint(lambda ethtype: ethtype <= 0x810 ,['type'])
        self.p.addConstraint(lambda len , type: len ==64 if type ==0x806 else True , ['length' ,'type']) 

    def solve(self):
        self.solutions = self.p.getSolutions()
        #print(self.solutions)
        for i in range(sys.getsizeof(self.solutions)):
            totalsols= i+1
        print(totalsols)

    def get(self):
        return random.choice(self.solutions)
        
if __name__== "__main__":
        const = etherconstr()
        const.p.addConstraint(lambda type: type==0x806 ,['type'])
        const.solve()
        for i in range(5):
            #print(i)
            print(f"{const.get()}")


from ioexpender import PCF8575

class keyboard_4plus4(object):

    def __init__(self,io:PCF8575,pinlist:list,keylist:list=[]):
        '''
        io:made with PCF8575
        pinlist:[C4,C3,C2,C1,R1,R2,R3,R4]
        '''
        self.io=io
        self.pre_status=0x0000

        self.col2pin=[pinlist[3],pinlist[2],pinlist[1],pinlist[0]]
        self.row2pin=[pinlist[4],pinlist[5],pinlist[6],pinlist[7]]

        self.USELIST=0x0000
        for i in pinlist:
            self.USELIST|=(1<<i)
            
        self.COLLIST=0x0000
        for i in self.col2pin:
            self.COLLIST|=(1<<i)

        self.ROWLIST=0x0000
        for i in self.row2pin:
            self.ROWLIST|=(1<<i)

        self.keylist=keylist

    def scan(self):
        # print('ss')
        self.io.writeN(self.USELIST,self.COLLIST)
        res=self.io.readN(self.USELIST)^self.COLLIST
        # print(bin(res))
        if(res):
            select_col=0
            for i in range(4):
                if res&(1<<self.col2pin[i]) :
                    select_col+=i+100        
            if(select_col>=200 or select_col==0):
                return 0
        else:
            self.pre_status=0x0000
            return 0
        
        self.io.writeN(self.USELIST,self.ROWLIST)
        res=self.io.readN(self.USELIST)^self.ROWLIST
        if(res):
            select_row=0
            for i in range(4):
                if res&(1<<self.row2pin[i]) :
                    select_row+=i+100
            if(select_row>=200 or select_row==0):
                return 0
        else:
            self.pre_status=0x0000
            return 0
        
        # print('s')
        # print(select_col)
        # print(select_row)
        select_id=select_row*4+select_col-500

        if(self.pre_status&(1<<select_id)):
            return 0
        else :
            self.pre_status=1<<select_id
            return select_id+1

    def get_key(self):
        if(len(self.keylist)!=16):
            raise Exception("please set keylist correctly when init the keyboard")
        else:
            ret=self.scan()
            if(ret):
                return self.keylist[ret-1]
            else:
                return 0
        
if __name__=="__main__":
    io=PCF8575(port=1,address=0x20)
    keylist=['1','2','3','quit',
             '4','5','6','back',
             '7','8','9','pgup',
             '.','0','enter','pgdn']
    k=keyboard_4plus4(io,[0,1,2,3,4,5,6,7],keylist=keylist)
    while(1):
        ret=k.get_key()
        if(ret):
            print(ret)
                
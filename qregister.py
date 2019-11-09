import qbit
class qregister:
    def __init__(self,*qbits):
        self.qbits = list(qbits)
        self.length = len(qbits)
        self.vector = qbit.cart_prod_qbits(qbits)
        

    @classmethod
    def __len__(cls):
        return cls.length


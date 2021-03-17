
class FakeDB:
    def __init__(self):
        self.store ={}

    def get_by_id(self,id:str) ->list:
        return self.store.get(id) if id in self.store else []

    def add(self,id:str,list_obj:list):
        self.store[id] = list_obj

    def get_all(self)->list:
        res=[]
        for k in self.store:
            res.extend(self.store[k])
        return res

    def filter(self,predicate)->list:
        return list(filter(lambda a : predicate(a), self.get_all()))

    def search_in_field(self,text:str,field:str)->list:
        return [rec for rec in self.get_all() if text in str(rec[field])]



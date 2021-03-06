import attrdict

class InventoryItem(attrdict.AttrMap):
    def __init__(self, *args, **kwargs):
        """Idea from http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python.

        Initialise with:
        >>> item = InventoryItem(item_json_dictionary)"""
        super(InventoryItem, self).__init__(*args, **kwargs)

    # def __repr__(self):
    #     return "InventoryItem"+"("+str(attrdict.AttrMap(self.__dict__))+")"
    
class Creature(attrdict.AttrMap):
    def __init__(self, *args, **kwargs):
        """Idea from http://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute-in-python.

        Initialise with:
        >>> item = Creature(item_json_dictionary)"""
        super(Creature, self).__init__(*args, **kwargs)

    def __str__(self):
        return "Creature"+"("+str(attrdict.AttrMap(self.__dict__))+")"

# Classes for piece and piece tuples
class Piece: 
   def __init__(self,owner, id):
      self.owner = owner
      self.id = id
      self.position = owner.starting_square

    
class PieceTuple:
   def __init__(self,owner,position,size):
      self.owner = owner
      self.position = position      
      self.size = size

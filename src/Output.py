
class Output:
  
  def __init__(self, outputfilename: str):
    self.file = open(f"./outputs/{outputfilename}.txt", "a")
  
  def write(self, string: str):
    self.file.write(string + "\n")
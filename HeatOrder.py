 
# HeatOrder script - reorder preheaters to make toolheads and bed heat up simultaneously
# Runs with the PostProcessingPlugin which is released under the terms of the AGPLv3 or higher.
# This script is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# 

from ..Script import Script

class HeatOrder(Script):
  def __init__(self):
      super().__init__()

  def getSettingDataString(self):
    return """{
      "name": "Heating Order",
      "key": "HeatOrder",
      "metadata": {},
      "version": 2,
      "settings": {
        "toolsimu":
        {
          "label": "Heat toolheads simultaneously",
          "description": "Heat toolheads simultaneously without waiting for each other",
          "type": "bool",
          "default_value": true
        },
        "bedsimu":
        {
          "label": "Heat bed simultaneously",
          "description": "Heat toolheads without waiting for the bed",
          "type": "bool",
          "default_value": true
        }
      }
    }"""

  def execute(self, data:list[str]):
    toolSimu = self.getSettingValueByKey("toolsimu")
    bedSimu = self.getSettingValueByKey("bedsimu")
    if not (toolSimu or bedSimu):
      return data
    for i, layer in enumerate(data):
      lines = layer.split("\n")
      preheatWaiters=[]
      indexToRemove=[]
      endIndex=0
      for i2, line in enumerate(lines):
        if (bedSimu and line.startswith("M190")) or (toolSimu and line.startswith("M109")):
          preheatWaiters.append(line)
          indexToRemove.append(i2)
          endIndex=i2
      for j in indexToRemove:
        lines[j]=";"+lines[j]
      for line2 in preheatWaiters:
        lines.insert(endIndex+1,line2)
      data[i] = "\n".join(lines)
    return data

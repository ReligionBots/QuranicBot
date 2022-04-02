import json
import utils as ut

lines = ut.readText("QuranicBot/Data/Text/q.txt")


print(lines.split("?")[0].split(":")[1].strip())
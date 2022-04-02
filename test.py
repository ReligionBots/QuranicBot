import requests as req
import json

localhost = "localhost:3003"

# def drop_lowest(scores, drop_number):
#     data = scores.copy()
#     index = 0
#     for i in data: 
#         print(i)
#         for y in i:
#             print(y)
            
#             for x in drop_number:
#                 print (y,x)
#                 if y == x:
#                     scores[index].pop(index)
#                     print("removed")
                
#             print("separated")
#         index = index + 1
#     print(scores)
    
#     pass

# scores = [[10,9, 7, 8],[1,2,1,0],[50,50,50,50],[75, 100]]
# drop_number = [1,2,1,0]
# drop_lowest(scores, drop_number)


getQ = req.get(f"http://{localhost}/quran/get")

print(json.loads(getQ.text))
# requestedData = json.loads(getQ.text)

# array = []

# for i in requestedData:
#     array = i['TranslationId'] 


# for i in array: 
#     try:
#         getQ = req.delete(f"http://localhost:3003/quran/delete/{i}/")
#         print(getQ)
#     except Exception as e:
#         print(e)
    


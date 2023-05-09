import json

def find_positions(data, symbols):
    positions = {symbol: [] for symbol in symbols}
    for i, line in enumerate(data):
        for j, char in enumerate(line):
            if char in positions:
                positions[char].append([j, i])
    return positions

def get_part(list, contain_y):
    tmp_list = []
    for i in list:
        for j in contain_y:
            tmp_list.append([i[1], j])
    return tmp_list

def create_json(length, sky, ground, gumba, coin, Qbox):
    jsonformat = {
        "id":0,
        "length":length,
        "level":{
            "objects": {
                "bush":[

                ],
                "sky": sky,
                "cloud":[

                ],
                "pipe":[
                    #[8,10,4],
                    #[12,12,4],
                    #[22,12,4],
                    #[29,9,6]
                ],
                "ground":ground
            },
            "layers": {
                "sky":{
                    "x":[0,length],
                    "y":[0,13]
                },
                "ground":{
                    "x":[0,length],
                    "y":[14,16]
                }
            },
            "entities": {
                "CoinBox":Qbox,
                "coinBrick":[
                    [37,9]
                ],
                "coin":coin,
                "Goomba":gumba,
                "Koopa":[

                ],
                "RandomBox":[
                  #[4, 3, "RedMushroom"],
                  #[52, 2, "RedMushroom"]
                ]
            }
        }
    }
    return jsonformat




data = [
    '----------------------------------------------------------------------------------------------------',
    'xxxxxxxxxxxx----------------------------------------------------------------------------------------',
    'SSSSSSSSSSSS-------------------------------SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS',
    '--------------------------------------------------SSS--SSSSSSS--SSSSS-------SSSS------SSSS--SS------',
    '--------------------------------------------------SSS--SSSSSSS--SSSSS--E----SSSS------SSSS--SS------',
    '------------------------------------------------SS----------SS----S----SS---------------SS----------',
    '------------------------------------------------SS----------SS----S----SS---------------SS---E------',
    '------------------------------------------------SS----------SS----S----SS-------------S-SS--<>------',
    '-------E----------------------------------------SS-----oooooSS----So??-SS----E--------SoSS--[]------',
    '------<>----------------------------QQQQ--------SSSSS--SSSSSSS----SSS--SS---SSSS------SSSS--XX------',
    '--XXX-[]--SS-------------------------------B------SSS---------------------EE---------------------xxx',
    'oxXXX-[]--SS---------------------B--E------b------SSS--------------------------xxxx-------------xx]-',
    'oQXXX-[]--SSxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx---xxxxxxxxxxxxxx-]-',
    'XXXX--XX--XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX---QXXXXXXXXXXXXXXXX'
]

symbols = ['x', 'S', 'E', 'o', '?', 'X', 'Q', 'B', 'b']

map_length = len(data[1])
sky = find_positions(data[13], "-")["-"]
sky = get_part(sky, [13, 14])
#print(sky)
ground  = find_positions(data, "S")["S"]
gumba = find_positions(data, "E")["E"]
coin = find_positions(data, "o")["o"]
Qbox = find_positions(data, "Q")["Q"]
jsonData = create_json(map_length, sky, ground, gumba, coin, Qbox)
filename = 'testJson/Test.json'
print(jsonData)
def save_to_json(jsonData, filename):
    with open(filename, 'w') as f:
        json.dump(jsonData, f)

save_to_json(jsonData, filename)
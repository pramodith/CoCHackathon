import json
class Expiry_date:

    def __init__(self):
        time=None
        '''
        self.expiry_dict={}
        with open("food_db/food_expiry.csv", 'r') as f:
            expiration_dates = f.read().split("\n")

        for line in expiration_dates:
            line=line.split(",")
            try:
                result=self.get_digits(line[1])
                if len(result)>0:
                    time=int(result[0])
                if "weeks" in line[1] or "week" in line[0]:
                    time*=7
                elif "month" in line[1]:
                    time*=30
                self.expiry_dict[line[0].strip()]=time
            except Exception as e:
                pass
        self.expiry_dict=json.dumps(self.expiry_dict,indent=3)
        with open("expiry_json.json",'w') as f:
            f.write(self.expiry_dict)
        '''

    def get_digits(self,text):
        return list(filter(str.isdigit, text))

    def get_expiry_date(self,food_item):
        with open("../food_db/expiry_json.json",'r') as f:
            dic=json.load(f)
            if food_item in dic:
                return dic[food_item]
            else:
                for key in dic.keys():
                    if food_item in key.lower():
                        return dic[key]


# c=Expiry_date()
# print(c.get_expiry_date('apples'))
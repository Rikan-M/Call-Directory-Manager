import json
import logging
import re
import os
logging.basicConfig(level=logging.INFO,filename="Call_Directory/Call_records.log",filemode="a", format='%(asctime)s - %(levelname)s - %(message)s')
class TrieNode:
    def __init__(self):
        self.children=[None]*26
        self.isleaf=False
class Trie_structure:
    def __init__(self):
        self.root=TrieNode()
    def clear(self):
        self.root=TrieNode()
    def insert(self,word:str):
        temp=self.root
        for letter in word:
            index=ord(letter)-ord('a')
            if temp.children[index] is None:
                temp.children[index]=TrieNode()
            temp=temp.children[index]
        temp.isleaf=True
    def search_forward(self,temp, prefix, results):
        if temp.isleaf:
            results.append(prefix)
        else:
            for l in range(26):
                self.search_forward(temp.children[l],prefix+ chr(l + ord('a')),results)
        
    def search(self,prefix):
        temp=self.root
        for letter in prefix:
            idx=ord(letter)-ord("a")
            if temp.children[idx] is not None:
                temp=temp.children[idx]   
            else:
                return []
        found=[]
        self.search_forward(temp,prefix,found)
        return found
        
class CallRecords:
    def __init__(self):
        self.records=load("Call_Directory/Phone_Call_Record_Data")
        self.Trie=Trie_structure()
        os.makedirs("Call_Directory", exist_ok=True)
    def create_trie(self):
        self.Trie.clear()
        if len(self.records)!=0:
            for name in self.records:
                self.Trie.insert(name)
    def number_validation(number):
        validate=re.fullmatch(r'[6-9][0-9]{9}',number)   
        if validate!=None:
            return True
        else:
            return False
    def insert(self,name,number):
        if self.records.get(name):
            return "The Name Already Exist ! try again"
        else:
            if self.number_validation(number):
                self.records[name]=number
                logging.info(f"New record added , {name} : {number}")
                self.create_trie()
                self.save_file()
                return "Account Created"
            else:
                return "Invalid Number"
    def save_file(self):
        save("Call_Directory/Phone_Call_Record_Data",self.records)
    def search(self,name):
        found=self.Trie.search(name)
        if len(found)==0:
            return None
        found_item=[(found_name,self.records[found_name]) for found_name in found]
        return found_item
    def delete(self,name):
        if self.records.get(name):
            number=self.records.pop(name)
            logging.info(f"Record deleted , {name} : {number}")
            self.create_trie()
            self.save_file()
            return f"Record deleted , {name} : {number}"
        return "No such data found"
    def show(self):
        return self.records
    def update(self,old_name,new_name=None,number=None):
        if self.records.get(old_name):
            if new_name==None:
                new_name=old_name
            if number==None:
                number=self.records[old_name]
            if self.number_validation(number):
                self.records.pop(old_name)
                self.records[new_name]=number
                self.create_trie()
                self.save_file()
                logging.info(f"The record {old_name} is updated to {new_name}:{number}")
                return f"The record {old_name} has been updated"
            return "Invalid number"
        return "No such data found"
            

def save(filename, value):
    with open(filename, 'w') as f:
        json.dump({'Data': value}, f)

def load(filename):
    try:
        with open(filename, 'r') as f:
            value = f.read()
            data = json.loads(value)
            if not data.get('Data', {}):
                logging.warning("Failed to restore data from file")
                return {}
            logging.info(f"Data loaded from {filename}")
            return data['Data']
    except (FileNotFoundError, json.JSONDecodeError):
        logging.warning("Failed to restore data from file")
        with open(filename, 'w') as f:
            f.write(json.dumps({'Data': {}}))
        return {}

callList=CallRecords()
print("To see call list press 1.")
print("To add new contact press 2.")
print("To delete a record press 3.")
print("To update a contact press 4.")
print("To search a contact press 5.")
print("To quit press 6.")
while True:
    user_choice=input("Enter your choice here : ")
    try:
        user_choice=int(user_choice)
        if 6<user_choice<1:
            print("Enter a valid choice")
    except:
        print("Enter a valid choice")
    if user_choice==1:
        print("_"*100)
        data=callList.show()
        for i in data:
            print(f"{i[0]} : {i[1]}")
        print("_"*100)
    elif user_choice==2:
        con_name=input("Enter the contact name : ").lower()
        con_number=input("Enter the contact number : ")
        confirmation=callList.insert(con_name,con_number)
        print(confirmation)
    elif user_choice==3:
        con_name=input("Enter the contact name : ").lower()
        confirmation=callList.delete(con_name)
        print(confirmation)
    elif user_choice==4:
        old_name=input("Enter the old name : ").lower()
        new_name=input("Enter the new name (or you can skip) : ").lower()
        con_number=input("Enter the contact's updated number (or you can skip) : ")
        if len(new_name)==0:
            new_name=None
        if len(con_number)==0:
            con_number=None
        confirmation=callList.update(old_name,new_name,con_number)
        print(confirmation)
    elif user_choice==5:
            search_name=input("Enter the name for search : ").lower()
            search_ids=callList.search(search_name)
            if search_ids is not None:
                for search_id in search_ids:
                    print('Name : ',search_id[0])
                    print('Number : ',search_id[1])
                    print("_"*100)
            else:
                print("No such data found")
    elif user_choice==6:
        break
#!/usr/bin/env python3

import csv
import random
from dataclasses import dataclass
from os import PathLike
from os.path import exists
from os.path import splitext
from collections import defaultdict
from pathlib import Path


condition_map = defaultdict(
    lambda: '',
    Mint="M",
    NearMint="NM",
    Excellent="NM",
    Good="LP",
    LightPlayed="MP",
    Played="HP",
    Poor="D"
    )

moxfield_headers = [
    "Count",
    "Name",
    "Edition",
    "Condition",
    "Language",
    "Foil",
    "Collector Number"
    ]


@dataclass(frozen=True, slots=True)
class CardData:
    quantity: str
    trade_quantity: str
    name: str
    set_code: str
    set_name: str
    collector_num: str
    condition: str
    foil: str
    language: str

    def get_output_dict(self) -> dict[str, str]:
        return {
            moxfield_headers[0]: self.quantity,
            moxfield_headers[1]: self.name,
            moxfield_headers[2]: self.set_code,
            moxfield_headers[3]: self.condition,
            moxfield_headers[4]: self.language,
            moxfield_headers[5]: self.foil,
            moxfield_headers[6]: self.collector_num
            }


def generate_cards(csv_path: PathLike) -> list[CardData]:
    retval: list[CardData] = []
    print("\nReading cards from your file...")
    with open(csv_path, 'r') as csv_file:
        # The first line is a seperator definition
        seperator = csv_file.readline().split('=')[1].strip('"\n')
        csv_reader = csv.DictReader(csv_file, delimiter=seperator)

        data_row: dict
        for data_row in csv_reader:
            # Dragon Shield adds a junk data row at the end
            if data_row['Quantity'] == '':
                continue

            printing = data_row['Printing'].lower()
            if printing not in ('etched', 'foil'):
                printing = ''

            card = CardData(
                data_row['Quantity'],
                data_row['Trade Quantity'],
                data_row['Card Name'],
                data_row['Set Code'],
                data_row['Set Name'],
                data_row['Card Number'],
                condition_map[data_row['Condition']],
                printing,
                data_row['Language'],
                )

            retval.append(card)

    return retval

def get_file_info(root):
    while True:
        filename = input("\nWhich file would you like to convert?: ")
        in_path = Path(str(root)+"\\"+filename)
        fileFound = exists(in_path)
        if fileFound:
            if random.random() > 0.9:
                print("\nKind of a weird file name...\nWhy would you call it that?")
            break
        else:
            print(f"\nFile not found. Make sure that file is in {root}\nDouble check that the file is a .csv and include \".csv\" at the end of the file name.\nTry again or press CTRL + C to quit.")
            continue
    return Path(filename), in_path
    pass

def convert_to_deck(in_path, out_path, card_data: CardData):
    # Headers:
    # Amount CardName (SetCode) Number *F*
    with open(out_path, 'w') as out_file:
        print("\nMoxifying decklist...")
        for card in card_data:
            out_file.write(card.quantity + " " + card.name + " (" + card.set_code + ") " + card.collector_num + (" *F*\n" if card.foil == "foil" else "\n"))
    pass

def convert_to_collection(in_path, out_path, card_data: CardData):
    with open(out_path, 'w', newline='') as out_file:
        writer = csv.DictWriter(out_file,
                                fieldnames=moxfield_headers,
                                dialect=csv.unix_dialect)
        writer.writeheader()
        print("\nMoxifying collection...")
        for card in card_data:
            writer.writerow(card.get_output_dict())
    pass

def get_again():
    while True:
        again = input("\nGot another file to moxify?\nJust type y or n: ").lower()
        if again == "y": break
        elif again == "n": break
        else:
            print("\nNeed help finding the y and n keys on the keyboard?\nIdiot.")
    return again

def count_cards(card_data: CardData):
    total = 0
    for card in card_data:
        total += int(card.quantity)
    print(f"\n{total} total cards found in {len(card_data)} rows.")
    if total == 100:
        print("Just the right amount of cards.")
    elif total == 101:
        print("Is that a mistake or do you have a Companion card in there?")
    elif total < 100:
        print("Not quite a complete deck yet.")
    elif total > 101:
        print("More than a full deck in there. Is that a sideboard or did ya fuck up?")
    
def print_logo():
    if bool(random.getrandbits(1)):
        print("""                                                                                                                                    
        @%%%%%%%%@      %@%%%%%@%@    @@@%%%%%%%%%@     @%@@%@@%%%%%@% @@@@@@@%=%  @%@*:%@@%@@=%    
       @@%-:-==:-%@    @%@==-::=@@   @%%@*::--=::=%@  @%-::::-*%:::::@@@%@:::=@% @%--:::@%@*--%%    
         @%+===-==%@      %@-==:@@      @@@%%#::::@@  %*::-:%@  @%@-%@   @@-=:%@ %:::::%@  %@#%     
         %@+=+===-=%@   @%@===-:-%@    %@-@% %=::::%@@%:=:-@@     %%@    @@::-%@@%.-:.%@   @@%@     
        @@-=@%@=-==+@@@@%%===++=-:%@  %@=-%%%@%::::%%@%:-::@@  @%%%@@@@@ @@-:-% @%:=-.%@            
       @%%%%% @%===-=@@=+%%%%++====%@%@==:-::%%@::::@@@@::::%@ %%@=::@%%@@@-::%@ %@--=:%@@  @@@@%%%@
       %==:%@  @%:-===:-=%@ @@==-=:%%%=-==-@%@@@-::::@@@%==--#@@%:::@@  @%::::=%@ %@-.--:-=+-:::-%@ 
      @@=-@@    @%==-==-%@   @@=--==@%@*@@#%  @%@%%%%@%@ @%@@#@%%%@:@@ @%:-@%%%@%  @%%%-:=%@%%%@@   
     @%-:@%      @@=-=-=@@    %*----=@@                           @@%@ @%%@                         
     %==-%        %==:==-%@   @%:-====%          
    %@==@@        @%====:@%    @@====-@%      ___                       _             __          _
  @%@:::-%@        %=---:-%@  @@-++====-@%@    | |_  _    |V| _     o _|_ o  _  __   (_  _  __ o |_)_|_
 %@=*@%%%%%        @@-==%%@ @%=+%@@%%%@@#=%@   | | |(/_   | |(_)><  |  |  | (/_ |    __)(_  |  | |   |_   
 @%@@              @@:@%     @%@        @@@                                                     
                     @@                                                                                                                                                                                
""")
    else:
        print("""                                                                                                                                                                                                                                                                                                                                    
            *                                                                                        
            *                                                                                        
        *   -   *                                                                                    
        +   -   +                                                                                    
        -   +*  =-                                                                                   
    *  +=  +*=  ==  *                                                                                
    *-  +*- +*=  *=  =*      ##***   ##%%*        ##****#       *%%%##*****    #****    *%%##***##*   
    +*- **++***+***  *+     ****##  *%%%%@       *** *##%%     %%##*     *     *##%*   %##**     #    
    ******************+     *#*##%% %%*%%%%     **#   %%%@%   #****            *%%%*  ***##           
      ***************      ##  %%%%@%  #%%##    #%     %%%%*  **###    @%%%%   *%%%*  ##%%%           
         +********        %%*   %%%%*   ####*  %%%%%    %###  ##%%%    *%%##   *%##*  *%@%%           
          +******        %%%     %%*     ###%* *@%%     *####  *%@%%*  *##*#   ####*    %%##*    %*   
           *****       *%@%%%*    #     %%%%%%%  %*     #%%%%%*   *####**##%  ###%%%*      #%%%*      
            **+        ___       ___           __         ___    ___  __      __   __   __     __  ___
             =          |  |__| |__      |\/| /  \ \_/ | |__  | |__  |__)    /__` /  ` |__) | |__)  |         
             *          |  |  | |___     |  | \__/ / \ | |    | |___ |  \    .__/ \__, |  \ | |     |
             *
             *                                                                                                                                                                                        
    """)

def main():
    root = Path(__file__).parent
    print_logo()
    print("\nThanks for using this super cool script to convert your Dragonshield files to ones Moxfield likes.")
    print("Press CTRL + C at any point to quit.")

    try:
        while True:
            filename, input_path = get_file_info(root)
            card_data = generate_cards(input_path)
            count_cards(card_data)
            deck_or_collection = input("\nEnter 'd' for deck, 'c' for collection, or 'dc' for both: ")
            if deck_or_collection == 'd':
                output_path = Path(f"moxifiedDeck-{filename.stem}.txt")
                convert_to_deck(input_path, output_path, card_data)
                print(f"\nA file called \"moxifiedDeck-{filename.stem}.txt\" has been placed here:\n{root}")

            elif deck_or_collection == 'c':
                output_path = Path(f"moxifiedCollection-{filename}")
                convert_to_collection(input_path, output_path, card_data)
                print(f"\nA file called \"moxifiedCollection-{filename}\" has been placed here:\n{root}")

            elif deck_or_collection in ('cd', 'dc'):
                if deck_or_collection == 'cd': print("\n\n\nYou must think you're pretty funny for typing 'cd' instead of 'dc',\nas if something so stupid could ever confuse me.")
                output_path = Path(f"moxifiedDeck-{filename.stem}.txt")
                convert_to_deck(input_path, output_path, card_data)
                print(f"\nA file called \"moxifiedDeck-{filename.stem}.txt\" has been placed here:\n{root}")
                output_path = Path(f"moxifiedCollection-{filename}")
                convert_to_collection(input_path, output_path, card_data)
                print(f"\nA file called \"moxifiedCollection-{filename}\" has been placed here:\n{root}")

            again = get_again()
            if again != 'y':
                print("\n\nSmell ya later, dingus.\n")
                break
    except KeyboardInterrupt:
        print("\n\nLater nerd.\n")

if __name__ == "__main__":
    main()

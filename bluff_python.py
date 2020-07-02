from random import shuffle
from collections import defaultdict


class bluff():

    def __init__(self, no_of_player=0):
        self.last_player_claiming_cards_record = ""
        self.last_player_throw_record = "player 0"
        self.last_player_name_throw_record = "player 0"
        self.no_of_player = no_of_player
        self.currentActivePlayer=""
        self.card_on_mat = ()
        self.player_info_json = defaultdict(object)
        self.cards = ['AS', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', '10S', 'JS', 'QS', 'KS', 'AH', '2H', '3H', '4H', '5H', '6H',
'7H', '8H', '9H', '10H', 'JH', 'QH', 'KH', 'AC', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', '10C', 'JC', 'QC', 'KC', 'AD',
'2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', '10D', 'JD', 'QD', 'KD']

    def shuffle_cards_fn(self, no_of_deck):
        self.shuffle_cards = self.cards * no_of_deck
        self.shuffle_cards = [x+"_"+str(i) for i,x in enumerate(self.shuffle_cards)] 
        self.total_no_of_cards = len(self.shuffle_cards)
        shuffle(self.shuffle_cards)
        print('self.shuffle_cards self.shuffle_cards cnnnn', self.shuffle_cards)

    def player_choice_after_distribution(self):
        player_choice = input(
            '\nchoose option   1.Throw cards \n\t\t2.Pick cards from mat \n\t\t3.Pass')
        return player_choice

    def card_distribution_to_player(self,playerDictionary):
        """
        card_distribution_to_player is distributing the cards according to number of players
        """
        print('card distribution fn called')
        no_of_card_to_single_player = int(
            self.total_no_of_cards/self.no_of_player)
        cards_left_after_distribution = self.total_no_of_cards % self.no_of_player
        starting_card = 0
        ending_card = no_of_card_to_single_player
        self.player_info_json["currentActivePlayer"] = "{} is in Action".format(playerDictionary["player 1"])
        self.player_info_json["currentActivePlayerNumber"] = "{}".format("player 1")
        for no_of_player_obj in range(self.no_of_player):
            player = 'player {}'.format(int(no_of_player_obj)+1)
            self.player_info_json[player]
            list_for_card_to_individual = []
            list_for_card_to_individual.extend(
                self.shuffle_cards[starting_card:ending_card])
            list_for_card_to_individual.sort()
            starting_card += no_of_card_to_single_player
            ending_card += no_of_card_to_single_player
            # list_for_card_to_individual.append(cards.pop())
            self.player_info_json[player] = {
                'total_cards': list_for_card_to_individual}
        return self.player_info_json

    # def shuffle_cards(self):
    # 	return shuffle(self.cards)
    
    def handlePass(self, playerInfo, userName,playerDictionary):
        calculateNextPlayer = int(playerInfo[7])+1
        if calculateNextPlayer>self.no_of_player:
                calculateNextPlayer=1
        self.player_info_json["currentActivePlayer"] = "{} is in Action".format(playerDictionary["player "+ str(calculateNextPlayer)])
        self.player_info_json["currentActivePlayerNumber"] = "{}".format("player "+ str(calculateNextPlayer))
        return self.player_info_json
    def pick_cards_from_mat(self, playerInfo, userName,playerDictionary):
        if userName=="":
            userName=playerInfo
        cheating = False
        try:
            pick_card_from_mat_list = list(self.card_on_mat)
            prev_player_cards_record = self.last_player_claiming_cards_record
            #print("prev_player_cards_record {}".format(prev_player_cards_record))
            last_cards_from_mat = pick_card_from_mat_list[-int(
            prev_player_cards_record[0]):]
            for cards_from_mat in last_cards_from_mat:
                #print("cards_from_mat[0]  {}  prev_player_cards_record {}".format(cards_from_mat[0], prev_player_cards_record[1]))
                if cards_from_mat[0] != prev_player_cards_record[1][0]:
                    cheating = True
            if cheating:
                self.player_info_json['{}'.format(
                    self.last_player_throw_record)]['total_cards'].extend(pick_card_from_mat_list)
                self.player_info_json["serverMessageFromBluff"]="{} caught {} as {} was bluffing".format(userName,self.last_player_name_throw_record,self.last_player_name_throw_record)
                self.player_info_json["currentActivePlayer"] = "{} is in Action".format(playerDictionary[playerInfo] or playerInfo)
                self.player_info_json["currentActivePlayerNumber"] = "{}".format(playerInfo)
            else:
                self.player_info_json['{}'.format(playerInfo)]['total_cards'].extend(pick_card_from_mat_list)
                self.player_info_json["serverMessageFromBluff"]="{} got {} to pick all cards from MAT".format(self.last_player_name_throw_record,userName)
                self.player_info_json["currentActivePlayer"] = "{} is in Action".format(self.last_player_name_throw_record or self.last_player_throw_record)
                self.player_info_json["currentActivePlayerNumber"] = "{}".format(self.last_player_throw_record)
            print('#############################', pick_card_from_mat_list)
            print('#############################', self.player_info_json['{}'.format(playerInfo)])
            self.card_on_mat = ()
            return self.player_info_json
        except:
            print('exception in pickup thread')

    def throw_cards(self, playerInfo,card_to_throw_from_server,claiming_cards,userName,playerDictionary):
        if userName=="":
            userName=playerInfo
        self.last_player_claiming_cards_record = claiming_cards.split("_")
        print("playerInfo {}".format(playerInfo))
        print("player_info_json {}".format(self.player_info_json))
        print("card_to_throw_from_server {}".format(card_to_throw_from_server))
        no_of_card_to_be_thrown = len(card_to_throw_from_server)
        calculateNextPlayer = int(playerInfo[7])+1
        # no_of_card_to_be_thrown =int(input('How many card {} wants to throw'.format(playerInfo)))
        thrown_card_list = []
        try:
            for card_dict in card_to_throw_from_server:
                # get_cards=input('throw {} card'.format(create_list_of_thrown_cards+1))
                thrown_card_list.append(card_dict["card"])
                self.player_info_json['{}'.format(
                    playerInfo)]['total_cards'].remove(card_dict["card"])
                #print("update crrrrdddd--------> {}".format(self.player_info_json))
                # playerInfo['total_cards'].remove(get_cards)
            length_of_thrown_cards = len(thrown_card_list)
            claimed_card = self.last_player_claiming_cards_record[1]
            self.player_info_json["serverMessageFromBluff"]="{} has thrown {} cards and claiming it's {} (i.e {} cards of {})".format(userName,length_of_thrown_cards,claimed_card,length_of_thrown_cards,claimed_card)
            if len(self.player_info_json['{}'.format(
                    playerInfo)]['total_cards'])==0:
                self.player_info_json["serverMessageFromBluff"]="{} has won the bluff".format(userName)
            if calculateNextPlayer>self.no_of_player:
                calculateNextPlayer=1
            self.player_info_json["currentActivePlayer"] = "{} is in Action".format(playerDictionary["player "+ str(calculateNextPlayer)] or "player "+ str(calculateNextPlayer))
            self.player_info_json["currentActivePlayerNumber"] = "{}".format("player "+ str(calculateNextPlayer))
        except:
            print('error')
        finally:
            self.update_cards_on_mat(thrown_card_list)
            self.player_info_json['{}'.format(playerInfo)].update(
                thrown_cards=thrown_card_list)
            return self.player_info_json

    def update_cards_on_mat(self, thrown_card_list):
        self.card_on_mat += tuple(thrown_card_list)
        print('update_cards_on_mat', self.card_on_mat)


# no_of_player = 4
# no_of_deck =1
# bluffw = bluff(no_of_player)
# bluffw.shuffle_cards_fn(no_of_deck)
# get_card_distribution_to_player = bluffw.card_distribution_to_player()

# for k,v in get_card_distribution_to_player.items():
#	print (f"{k} - {v}")

# player_choice = bluffw.player_choice_after_distribution()
# if player_choice == '1':
#	bluffw.throw_cards(list(get_card_distribution_to_player.keys())[0])
#	bluffw.throw_cards(list(get_card_distribution_to_player.keys())[1])
# elif player_choice == '2':
#	bluffw.pick_cards_from_mat(list(get_card_distribution_to_player.keys())[1])
# else:
#	pass

    # """
    # done

    # 1. distribution of card
    # 2. throw card on mat by individual
    # 3. pickup card from mat
    # 4. pickup card from mat by individual
    # 5. no. of decks to be included

    # to be done
    # 1.
    # 2.

    # """

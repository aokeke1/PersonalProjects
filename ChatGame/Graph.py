# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 19:58:30 2017

@author: arinz
"""
import networkx as nx
import matplotlib.pyplot as plt
import random

class Game:
    def __init__(self,players=None,connections=None, winners = None,losers = None):
        self.game_graph = nx.Graph()
        self.game_digraph = nx.DiGraph()
        if players is not None:
            self.game_graph.add_nodes_from(players)
            self.game_digraph.add_nodes_from(players)
        if connections is not None:
            self.game_graph.add_edges_from(connections)
            self.game_digraph.add_edges_from(connections)
        if winners is not None:
            if type(winners)==tuple or type(winners)==set or type(winners)==list:
                self.winners = set(winners)
            else:
                self.winners = set()
                self.winners.add(winners)
        else:
            self.winners = set()
        if losers is not None:
            if type(losers)==tuple or type(losers)==set or type(losers)==list:
                self.losers = set(losers)
            else:
                self.losers = set()
                self.losers.add(losers)
        else:
            self.losers = set()
        self.update_players()
        
    def add_player(self,name):
        self.game_graph.add_node(name)
        self.game_digraph.add_node(name)
    def add_connection(self,start,end):
        self.game_graph.add_edge(start,end)
        self.game_digraph.add_edge(start,end)
    def show_graph(self):
        winners = list(self.winners)
        losers = list(self.losers)
        remainder = list(set(self.game_graph.nodes())-self.winners-self.losers)
        pos=nx.spring_layout(self.game_graph) # positions for all nodes
        nx.draw_networkx_nodes(self.game_digraph,pos,
                               nodelist=losers,
                               node_color='r',
                               node_size=50, with_labels=True,
                           alpha=0.8)
        nx.draw_networkx_nodes(self.game_digraph,pos,
                               nodelist=winners,
                               node_color='g',
                               node_size=50, with_labels=True,
                           alpha=0.8)
        nx.draw_networkx_nodes(self.game_digraph,pos,
                               nodelist=remainder,
                               node_color='b',
                               node_size=50, with_labels=True,
                           alpha=0.8)
        nx.draw_networkx_edges(self.game_digraph,pos,width=1.0,alpha=0.5)
        nx.draw_networkx_labels(self.game_digraph,pos,font_size=16)
        #nx.draw(self.game_digraph, with_labels=True, font_weight='bold')
    def get_winners(self):
        return self.winners
    def update_winners(self):
        hasChanged = False
        concomps = list(nx.connected_components(self.game_graph))
        for cc in concomps:
            if (len(self.winners.intersection(cc))>0) and (len(cc.difference(self.winners))>0):
                self.winners.update(cc)
                hasChanged = True
        return hasChanged
    
    def get_losers(self):
        return self.losers
    def get_neutral(self):
        return set(self.game_graph.nodes())-self.winners-self.losers
    def update_losers(self):
        #losers can't also be winners
        hasChanged = False
        if len(self.winners.intersection(self.losers))>0:
            hasChanged = True
        self.losers -= self.winners
        possible_losers = self.get_neutral()
        for n in possible_losers:
            try:
                cycle = nx.find_cycle(self.game_digraph,n)
                self.losers.add(n)
                hasChanged = True
            except:
                continue
        possible_losers = self.get_neutral()
        for n in possible_losers:
            shortest_paths = nx.single_source_shortest_path(self.game_digraph,n)
            connected_losers = set(shortest_paths.keys()).intersection(self.losers)
            if len(connected_losers)>0:
                self.losers.add(n)
        return hasChanged
        
    def update_players(self):
        self.update_winners()
        self.update_losers()
    def add_random_edge(self):
        possible_starts = self.get_neutral()
        start = random.choice(list(possible_starts))
        possible_ends = set(self.game_graph.nodes()) - {start}
        end = random.choice(list(possible_ends))
        self.add_connection(start,end)
        self.update_players()
        return (start,end)
    def add_random_edge_smart(self):
        possible_starts_pre = self.get_neutral()
        possible_starts = set()
        for n in possible_starts_pre:
            if self.game_digraph.out_degree(n)==0:
                possible_starts.add(n)
        if len(possible_starts)==0:
            return None
        possible_ends = set()
        while len(possible_ends)==0:
            
            start = random.choice(list(possible_starts))
            possible_ends = set(self.game_graph.nodes()) - {start} - set(self.game_graph.adj[start].keys())
            if len(possible_ends)==0:
                possible_starts.remove(start)
                if len(possible_starts)==0:
                    return None
        end = random.choice(list(possible_ends))
        self.add_connection(start,end)
        self.update_players()
        return (start,end)
    
    def add_and_show(self):
        new_connection = self.add_random_edge_smart()
        self.show_graph()
        return new_connection


def make_sample_connections(sample_players,n,winner=[],losers=[]):
    has_out_degree = set()
    sample_connections = set()
    while len(sample_connections)<n:
        potential_pair = tuple(random.sample(sample_players,2))
        if (potential_pair[0] not in winner) and (potential_pair[0] not in losers) and (potential_pair[0] not in has_out_degree):
            sample_connections.add(potential_pair)
            has_out_degree.add(potential_pair[0])
    return sample_connections

#random.seed(0)
#sample_players = ['sam','lisa','mike','frank','josh','carly','nancy','tina']
#sample_players = list(range(20))
#sample_winners = random.sample(sample_players,1)
#remaining_players = list(set(sample_players)-set(sample_winners))
#sample_losers = random.sample(remaining_players,0)
#n = len(sample_players)/3
#sample_connections = make_sample_connections(sample_players,n,sample_winners,sample_losers)
#myGame = Game(sample_players,sample_connections,sample_winners,sample_losers)
#myGame.show_graph()
#myGame.update_players()

def create_samples(num_players=20,num_winners=1,num_losers=0):
    sample_players = list(range(num_players))
    sample_winners = random.sample(sample_players,num_winners)
    remaining_players = list(set(sample_players)-set(sample_winners))
    sample_losers = random.sample(remaining_players,num_losers)
    return sample_players,sample_winners,sample_losers

def play_one_round(num_players=20,num_winners=1,num_losers=0,showResult = True):
    sample_players,sample_winners,sample_losers = create_samples(num_players,num_winners,num_losers)
    tGame = Game(sample_players,None,sample_winners,sample_losers)
    update = tGame.add_random_edge_smart()
    while update is not None:
        update = tGame.add_random_edge_smart()
    numWinners = len(tGame.winners)
    numLosers = len(tGame.losers)
    if showResult:
        tGame.show_graph()
    return numWinners,numLosers
    
def playNRounds(n=1000,num_players=20,num_winners=1,num_losers=0):
    numWinnersTotal = 0
    numLosersTotal = 0
    for i in range(n):
#        if i%(n//20)==0:
#            print ((100*(i+1)/(n+1)),"% complete with testing")
        numWinners,numLosers = play_one_round(num_players,num_winners,num_losers,False)
        numWinnersTotal += numWinners
        numLosersTotal += numLosers
        
    numWinnersAvg = numWinnersTotal/n
    numLosersAvg = numLosersTotal/n
    results = {"win_total":numWinnersTotal,"win_avg":numWinnersAvg,"win_percent":100*numWinnersTotal/(numWinnersTotal+numLosersTotal),
               "lose_total":numLosersTotal,"lose_avg":numLosersAvg,"lose_percent":100*numLosersTotal/(numWinnersTotal+numLosersTotal)}
    return results

#print (playNRounds())
from collections import deque


class GraphSearcher:
    def __init__(self):
        self.visited = set()
        self.order = []

    def visit_and_get_children(self, node):
        """ 
        Leave this method as is! It will be over-written the child classes
        Each child class should perform the following:
            Record the node value in self.order AND return its children
            parameter: node
            return: children of the given node
        """
        raise Exception("must be overridden in sub classes -- don't change me here!")
    
    # depth-first search
    def dfs_search(self, node): 
        # 1. clear out visited set and order list
        self.visited = set()
        self.order = []
        # 2. start recursive search by calling dfs_visit
        self.dfs_visit(node)

    def dfs_visit(self, node):
        # 1. if this node has already been visited, just `return` (no value necessary)
        if node in self.visited:
            return
        # 2. mark node as visited by adding it to the set
        else:
            self.visited.add(node)
        # 3. call self.visit_and_get_children(node) to get the children
        children = self.visit_and_get_children(node)
        # 4. in a loop, call dfs_visit on each of the children
        for child in children:
            self.dfs_visit(child)
    
    # breadth-first search
    def bfs_search(self, node):
        """
        Efficient implementation using deque instead of list.
        Iterative / non recursive method.
        Top-down. Always starting from row '0'.
        """
        self.order = []
        to_visit = deque([node])
        added = {node}
        
        while len(to_visit) > 0:
            # 1. induct curr node into queue
            curr_node = to_visit.popleft()   # Fast O(1) operation
            ##print("CURR:", curr_node, end=" ")
            
            # 2. induct curr node children into queue
            curr_node_children = self.visit_and_get_children(curr_node)
            ##print("CURR children:", curr_node_children)
            for child in curr_node_children:
                if child not in added:
                    to_visit.append(child)
                    added.add(child)
            
            #print("TO VISIT:", to_visit)
            

class MatrixSearcher(GraphSearcher):
    def __init__(self, df):
        super().__init__() # call constructor method of parent class
        self.df = df
    
    def visit_and_get_children(self, node):
        # record the node value in self.order
        self.order.append(node)
        children = []
        # use self.df to determine what children the node has and append them
        for child, has_edge in self.df.loc[node].items():
            if has_edge:
                children.append(child)
        return children
        

class FileSearcher(GraphSearcher):
    def __init__(self):
        super().__init__() # call constructor method of parent class
        
    def visit_and_get_children(self, node):
        # open node
        with open(node, encoding='utf-8') as f:
            # record the file value
            self.order.append(f.readline().rstrip('\n'))
            # record the children
            children = f.readline().rstrip('\n').split(',')
        return children
    
    def concat_order(self):
        return "".join(self.order)

        
from selenium.webdriver.common.by import By
from io import StringIO
import pandas as pd
from time import sleep
import requests

class WebSearcher(GraphSearcher):
    def __init__(self, driver):
        super().__init__() # call constructor method of parent class
        self.driver = driver
        self.fragments = []
    
    def get_children(self, url):
        """
        Finds all hyperlinks in the given url by sending GET request and parsing page source.
        Returns a list of children URLs.
        """
        # 1. visit node (url) and return other urls/hyperlinks
        self.driver.get(url)
        children = []
        for a_element in self.driver.find_elements("tag name", "a"):
            children.append(a_element.get_attribute("href"))
        return children
    
    def visit_and_get_children(self, url):
        # 1. visit node (url) and record
        self.order.append(url)
        children = self.get_children(url)
        # 2. use pd.read_html() to get table fragments and store in attribute
        frag = pd.read_html(StringIO(self.driver.find_element("id", "locations-table").get_attribute("outerHTML")))[0]
        self.fragments.append(frag)
        # 3. return children
        return children
    
    def table(self):
        df = pd.DataFrame()
        for frag in self.fragments:
            df = pd.concat([df, frag], ignore_index=True)
        return df

def reveal_secrets(driver, url, travellog):
    # 1. assemble password
    pwd = travellog['clue'].astype("str").to_list()
    
    # 2. visit url
    driver.get(url)
    
    # 3. send password
    pwd_receiver = driver.find_element("id", "password-textbox")
    pwd_receiver.send_keys(pwd)
    
    # submit password
    go_button = driver.find_element("id", "submit-button")
    go_button.click()
    
    # 4. wait for webpage to load
    sleep(1)
    
    # 5. view location
    view_location_button = driver.find_element("id", "location-button")
    view_location_button.click()
    
    # wait for webpage to load
    sleep(1)
    
    #print(driver.page_source)
    # 6. capture image that appears
    image_tag = driver.find_element("id", "image")
    image_src = image_tag.get_attribute("src")
    
    # download secret image and save
    download_file(image_src)
    
    # 7. return current location
    secret_location = driver.find_element("id", "location").text
    return secret_location
    

def download_file(url):
    local_filename = "Current_Location.jpg"
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
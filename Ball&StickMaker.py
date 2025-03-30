import networkx as nx
import os
import matplotlib.pyplot as plt

G = nx.MultiDiGraph(format='png', directed=True)


def file_namer(title):
    s = 0
    file_name = title + str(s)

    for filename in os.listdir("Plots"):
        sf = os.path.join("Plots", filename)
        if os.path.isfile(sf):
            s += 1
            file_name = title + str(s)
            pass
        else:
            break
            pass

    return file_name


def readconnections(filename: str, x: int):
    with open(filename, "r") as f:
        lines = f.readlines()
        params = lines[0].rstrip()

        if params.__contains__("Topology: " + str(x)):  # if file contains network for topology being looked at
            for line in lines:  # go through the lines of the file
                edges = []
                conmatrix = []
                line = line.rstrip()  # remove trailing characters
                if line.__contains__("Best Layout: "):  # if line contains the 'Best Layout: '
                    cons = line.split(": ")  # retrieve the connections
                    maxele = 0  # variable for tracking the max number of elements for the row
                    count = 0  # counts the number of connections added to a row
                    connections = []  # records the connections in the row
                    for c in cons[1].split(" "):  # convert the string into the connections matrix
                        if count < maxele:  # if the count is less then max number of elements allowed in the row
                            connections.append(c)  # append the connection character to row
                            count += 1  # increment the count by one
                        else:  # else count has reached maximum
                            conmatrix.append(connections)  # append the row to the connection matrix
                            connections = [c]  # reset the row and add the character to the row
                            count = 1  # reset the count to only one character being in the row
                            maxele += 1  # increase max amount of characters in row by one
                    conmatrix.append(connections)  # add the last row of connections to the connections matrix

                    y = 0  # track the row being looked at in the connections matrix
                    for row in conmatrix:  # go through the rows of the connections matrix
                        x = 0  # track the column being looked at in the connection matrix
                        for edge in row:  # go through the columns of the connection matrix
                            # if there is a connection at the position being looked at in matrix,
                            # and it is not a connection between the edge and cloud
                            if edge == '1' and (y < 30 or x >= 1):
                                edges.append((y + 1, x + 1))  # record which nodes are being connected
                            x += 1  # increment the column position after examining a column
                        y += 1  # increment the row position after examining a row

                    layout = dict((n, G.nodes[n]["pos"]) for n in G.nodes())

                    color_map = []
                    for node in G:
                        if int(node) < 2:
                            color_map.append('blue')
                        elif int(node) > 31:
                            color_map.append('green')
                        else:
                            color_map.append("gray")

                    ax = plt.gca()
                    for edge in edges:
                        if edge[0] < 2 or edge[1] < 2:
                            ax.annotate("",
                                        xy=layout[str(edge[0])], xycoords='data',
                                        xytext=layout[str(edge[1])], textcoords='data',
                                        arrowprops=dict(arrowstyle="->", color="blue",
                                                        shrinkA=5, shrinkB=5,
                                                        patchA=None, patchB=None,
                                                        connectionstyle="arc3,rad=-0.3",
                                                        ),
                                        )
                        elif edge[0] > 31 or edge[1] > 31:
                            ax.annotate("",
                                        xy=layout[str(edge[0])], xycoords='data',
                                        xytext=layout[str(edge[1])], textcoords='data',
                                        arrowprops=dict(arrowstyle="->", color="green",
                                                        shrinkA=5, shrinkB=5,
                                                        patchA=None, patchB=None,
                                                        connectionstyle="arc3,rad=-0.3",
                                                        ),
                                        )
                        else:
                            ax.annotate("",
                                        xy=layout[str(edge[0])], xycoords='data',
                                        xytext=layout[str(edge[1])], textcoords='data',
                                        arrowprops=dict(arrowstyle="->", color="0.5",
                                                        shrinkA=5, shrinkB=5,
                                                        patchA=None, patchB=None,
                                                        connectionstyle="arc3,rad=-0.3",
                                                        ),
                                        )
                    nx.draw(G, pos=layout, node_color=color_map, with_labels=True, node_size=300)
                    title = file_namer("Graph")
                    plt.savefig("Plots/"+title+".png", format="PNG")
                    ax.clear()


def readlayout(filename: str):
    with open(filename, "r") as f:  # open the file and read from it
        lines = f.readlines()  # read all the lines from the file

        names = []
        network = []

        y = 0  # value recording the row the node is on

        for line in lines:  # go through each line of text from lines one by one
            x = 0  # value recording the column the node is located on
            line = line.rstrip().split("\t")  # remove trailing characters and split based on tab character
            for char in line:  # for every character in the line
                if char != '0':  # if the character is non-zero (i.e. a tower)
                    names.append(char)  # record the tower number
                    network.append((y, x))  # record the position of the tower
                x += 1
            y += 1

        for index, name in enumerate(names):
            G.add_node(name, pos=network[index])
        pass


def main():
    plt.figure("My graph Test")
    directory = 'Output'
    directory2 = 'Topologies'
    top = 0

    for filename in os.listdir(directory2):
        topology = os.path.join(directory2, filename)
        if os.path.isfile(topology):
            G.clear()
            readlayout(topology)
        for filename2 in os.listdir(directory):
            f = os.path.join(directory, filename2)
            if os.path.isfile(f):
                readconnections(f, top)
        top += 1


if __name__ == "__main__":
    main()

import wikipedia


# Non-recursive Breadth-first Search Implementation
def wikipedia_game(root, target):
    print("Finding path between %s and %s\n" % (root, target))
    root_page = wikipedia.page(root)
    G = {}
    G[root_page.title] = {
        'title': root_page.title,
        'distance': 0,
        'parent': None
    }
    Q = [G[root_page.title]]
    while Q:
        current = Q[0]
        Q = Q[1:]
        current_page = wikipedia.page(current['title'])
        print(current_page.title)
        for link in current_page.links:
            if link not in G:
                G[link] = {
                    'title': link,
                    'distance': current['distance'] + 1,
                    'parent': current
                }
                if link == target:
                    print("Found", target + "!")
                    print("Data:", G[link])
                    return
                Q.append(G[link])

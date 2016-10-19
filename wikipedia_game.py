import os, sys, wikipedia


def print_path(data):
    if data['parent']:
        print_path(data['parent'])
        print(' => ', end='')
    print(data['title'], end='')


def get_selection(selection):
    page = None
    while not page:
        try:
            entry = input('%s page title: ' % selection)
            page = wikipedia.page(entry)
        except wikipedia.exceptions.DisambiguationError as e:
            print('\nDisambiguation Selection (Choose one of these or use another term)')
            for option in e.options:
                print('\t' + option)
            print()
        except wikipedia.exceptions.PageError as e:
            print('Page error, try again.')
        except KeyboardInterrupt:
            print('Exiting')
            sys.exit()
    return page


# Non-recursive Breadth-first Search Implementation
def wikipedia_game():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Wikipedia Game\n\n')
    root_page = get_selection('Root')
    target_page = get_selection('Target')
    G = {}
    G[root_page.title] = {
        'title': root_page.title,
        'distance': 0,
        'parent': None
    }
    Q = [G[root_page.title]]
    print('\nFinding the path between the %s and %s pages...' %(root_page.title, target_page.title))
    while Q:
        current = Q[0]
        Q = Q[1:]
        try:
            current_page = wikipedia.page(current['title'])
            print('\t%s' % current_page.title)
            for link in current_page.links:
                if link not in G:
                    G[link] = {
                        'title': link,
                        'distance': current['distance'] + 1,
                        'parent': current
                    }
                    if link == target_page.title:
                        print('\n%s found!' % link)
                        print('Path: ', end='')
                        print_path(G[link])
                        print()
                        sys.exit()
                    Q.append(G[link])
        except wikipedia.exceptions.DisambiguationError as e:
            # Disambiguation Page
            G[e.title] = {
                'title': e.title,
                'distance': current['distance'] + 1,
                'parent': current
            }
            # Adds every link on disambiguation page to queue
            for option in e.options:
                if option not in G:
                    G[option] = {
                        'title': option,
                        'distance': current['distance'] + 2,
                        'parent': G[e.title] 
                    }
                    if option == target_page.title:
                        print('\n%s found!' % option)
                        print('Path: ', end='')
                        print_path(G[option])
                        print()
                        sys.exit()
                    Q.append(G[option])
        except wikipedia.exceptions.PageError as e:
            # Skips over the item in the queue if it results in a page error.
            print('\tSkipping %s...\n\t\t%s' % (current['title'], e))
        except KeyboardInterrupt:
            print('Exiting')
            sys.exit()


wikipedia_game()

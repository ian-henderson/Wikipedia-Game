import os
import sys

import wikipedia


def get_algorithm():

    print('Enter selection for an algorithm.')
    print('\t(1) Breadth-first Search')
    print('\t(2) Depth-first Search')
    print('\t(3) Iterative Deepening Depth-first Search')
    print('\n\tSelection: ')


def get_page(page_type):

    page = None

    while not page:

        try:
            entry = input('Enter %s page title: ' % page_type)
            page = wikipedia.page(entry)

        except wikipedia.exceptions.DisambiguationError as e:
            print('\nDisambiguation Selection (Choose one of these or use\
                    another term)')
            for option in e.options:
                print('\t' + option)
            print()

        except wikipedia.exceptions.PageError:
            print('Page error, try again.')

        except KeyboardInterrupt:
            print('Exiting')
            sys.exit()

    return page


def print_path(data):

    if data['parent']:
        print_path(data['parent'])
        print(' => ', end='')

    print(data['title'], end='')


# https://en.wikipedia.org/wiki/Breadth-first_search
def breadth_first_search():


# https://en.wikipedia.org/wiki/Depth-first_search
def depth_first_search():


# https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search
def iterative_deepining_depth_first_search():


def wikipedia_game():

    # Clears up the screen on start.
    os.system('cls' if os.name == 'nt' else 'clear')

    print('Wikipedia Game\n\n')

    root_page = get_page('root')
    target_page = get_page('target')

    # TODO: test to see if G = {} is needed.
    G = {}
    G[root_page.title] = {
        'title': root_page.title,
        'distance': 0,
        'parent': None
    }

    Q = [G[root_page.title]]

    print('\nFinding the path between the %s and %s pages...'
          % (root_page.title, target_page.title))

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

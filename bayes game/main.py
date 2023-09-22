import sys
import random
import itertools
import numpy as np
import cv2 as cv
from bayes import *

def main():
    app = Search('Cape_Python')
    app.draw_map(last_known_location=(160, 290))
    sailor_x, sailor_y = app.sailor_final_location(number_of_search_areas=3)
    print("-" * 65)
    print("\nInitial probability estimation (P):")
    print(f"P1 = {app.probability_area1:.3f}, P2 = {app.probability_area2:.3f}, P3 = {app.probability_area3:.3f}")
    search_number = 1

    while True:
        app.calculate_effectiveness()
        draw_menu(search_number)
        choice = input("Choose an option: ")

        if choice == "0":
            sys.exit()

        elif choice == "1":
            results_1, coords_1 = app.conduct_search(1, app.search_area1, app.effectiveness1)
            results_2, coords_2 = app.conduct_search(1, app.search_area1, app.effectiveness1)
            app.effectiveness1 = (len(set(coords_1 + coords_2))) / (len(app.search_area1)**2)
            app.effectiveness2 = 0
            app.effectiveness3 = 0

        elif choice == "2":
            results_1, coords_1 = app.conduct_search(2, app.search_area2, app.effectiveness2)
            results_2, coords_2 = app.conduct_search(2, app.search_area2, app.effectiveness2)
            app.effectiveness1 = 0
            app.effectiveness2 = (len(set(coords_1 + coords_2))) / (len(app.search_area2)**2)
            app.effectiveness3 = 0

        elif choice == "3":
            results_1, coords_1 = app.conduct_search(3, app.search_area3, app.effectiveness3)
            results_2, coords_2 = app.conduct_search(3, app.search_area3, app.effectiveness3)
            app.effectiveness1 = 0
            app.effectiveness2 = 0
            app.effectiveness3 = (len(set(coords_1 + coords_2))) / (len(app.search_area3)**2)

        elif choice == "4":
            results_1, coords_1 = app.conduct_search(1, app.search_area1, app.effectiveness1)
            results_2, coords_2 = app.conduct_search(2, app.search_area2, app.effectiveness2)
            app.effectiveness3 = 0

        elif choice == "5":
            results_1, coords_1 = app.conduct_search(1, app.search_area1, app.effectiveness1)
            results_2, coords_2 = app.conduct_search(3, app.search_area3, app.effectiveness3)

        elif choice == "6":
            results_1, coords_1 = app.conduct_search(2, app.search_area2, app.effectiveness2)
            results_2, coords_2 = app.conduct_search(3, app.search_area3, app.effectiveness3)

        elif choice == "7":
            main()

        else:
            print("\nImproper choice.", file=sys.stderr)
            continue

        # Uses Bayes' theorem to update the probability.
        app.revise_target_probs()

        print(f"\nAttempt number {search_number} - result: {results_1}", file=sys.stderr)
        print(f"\nAttepmt number {search_number} - result: {results_2}", file=sys.stderr)
        print(f"\nEffectiveness of the search (E) for attempt numer {search_number}")
        print(f"E1 = {app.effectiveness1:.3f}, E2 = {app.effectiveness2:.3f}, E3 = {app.effectiveness3:.3f}")

        if results_1 == 'Not found.' and results_2 == 'Not found.':
            print("\nNew probability estimation (P) "
                  f"for attempt number {search_number + 1}")
            print(f"P1 = {app.probability_area1:.3f}, P2 = {app.probability_area2:.3f}, P3 = {app.probability_area3:.3f}")

        else:
            cv.circle(app.image, (sailor_x[0], sailor_y[0]), 3, (255, 0, 0), -1)
            cv.imshow('Areas to be searched', app.image)
            cv.waitKey(1500)
            main()
        search_number += 1

if __name__ == '__main__':
    main()
